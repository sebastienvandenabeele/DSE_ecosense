from tracemalloc import start
import folium
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def nearest_point(x,arr):
    LSE = np.sum((arr-x)**2,axis=1)
    return arr[np.argwhere(LSE==np.min(LSE))][0][0]

def lat_long_to_scale(lat,long,dX,dY):
    dx,dy = dX*(long-120),dY*(lat+30)
    return np.abs(dx),np.abs(dy)

def moving_average(x, w):
    return np.convolve(x, np.ones(w), mode='same') / w

def flight_path_point(location,sensor_points,start_point,spacing,lat_or,lon_or):
    sensor_points = sensor_points.T
    points = [start_point]
    lat,lon = start_point
    lon_dir = lon_or 
    L = 10
    arg = np.argwhere(np.sum((sensor_points-start_point)**2,axis=1)==np.min(np.sum((sensor_points-start_point)**2,axis=1)))[0][0]
    left_points = sensor_points[np.argwhere(sensor_points[:,1] == np.min(sensor_points[:,1])).flatten()]
    left_points = left_points[left_points[:,0].argsort()][::-1]

    right_points = sensor_points[np.argwhere(sensor_points[:,1] == np.max(sensor_points[:,1])).flatten()]
    right_points = right_points[right_points[:,0].argsort()][::-1]
    flight_points = np.array([start_point])
    if lat_or == -1 and lon_or == -1:
        for i in range(int(L/spacing)):
            left = left_points[2*i:2*i+2]
            flight_points = np.vstack((flight_points,left))
            right = right_points[2*i+1:2*i+3]
            flight_points = np.vstack((flight_points,right))
        
    return flight_points

def flight_map(location,map,outer_points,sensor_points,spacing):
    park_perimeter = pd.read_excel(r"./data/park_perimeter.xlsx")
    park_perimeter.set_index("loc",inplace=True)
    ground_station = list(park_perimeter.loc["Launch site"].values)
    nearest_corner = nearest_point(ground_station,outer_points)

    if nearest_corner[0]<ground_station[0]:
        lat_or = -1
    else:
        lat_or = 1
    
    if nearest_corner[1]<ground_station[1]:
        lon_or = -1
    else:
        lon_or = 1
    
    flight_path_points = flight_path_point(location,sensor_points,nearest_corner,spacing,lat_or,lon_or)
    flight_path_points = np.vstack((ground_station,flight_path_points))
    flight_path_points = np.vstack((flight_path_points,ground_station))
    flight_path_ = folium.PolyLine(flight_path_points, color="yellow", weight=2.5, opacity=1).add_to(map)
    map.save("flight_path.html")
    print(flight_path_points)
    return map,flight_path_points

def flight_analysis(flight_points,topography,dX,dY,dL,cruise_alt,cruise_V,plot):
    h,V = cruise_alt,cruise_V
    lat,long = lat_long_to_scale(flight_points[:,0], flight_points[:,1],dX,dY)
    scaled_coordinates = np.hstack((lat.reshape((len(lat),1)),long.reshape((len(long),1))))
    all_points = np.array([0,0])
    for index,coord in enumerate(scaled_coordinates):
        if index<len(scaled_coordinates)-1:
            next_coord = scaled_coordinates[index+1,:]
            x_diff,y_diff = int(abs(next_coord[0]-coord[0])),int(abs(next_coord[1]-coord[1]))
            diff = np.maximum(x_diff,y_diff)
            x_range = np.linspace(coord[0],next_coord[0],diff)
            y_range = np.linspace(coord[1],next_coord[1],diff)
            inter_coords = np.hstack((x_range.reshape((diff,1)),y_range.reshape((diff,1))))
            all_points = np.vstack((all_points,inter_coords))
    
    index_points = np.array(pd.DataFrame(all_points[1:,:],columns = ["X","Y"]),dtype=int)
    elevation = topography[index_points[:,1],index_points[:,0]]
    elevation_ma = moving_average(elevation,100)
    flight = 1000*(dL/dX)*np.arange(len(elevation))
    print(np.shape(flight),np.shape(elevation_ma))

    climb_angle = (10/180)*np.pi
    top = np.arctan(climb_angle)*flight[int(len(elevation)/2)]
    ac_flight = np.linspace(0,top,int(len(elevation)/2)+1)
    desc_flight = np.linspace(top,0,int(len(elevation)/2))
    ac_arg = np.argwhere(ac_flight>cruise_alt)[0][0]
    desc_arg = np.argwhere(desc_flight<cruise_alt)[0][0]+len(ac_flight)
    elevation_ma[:ac_arg] = elevation[0]
    elevation_ma[desc_arg:] = elevation[-1]
    flight = np.append(ac_flight,desc_flight)
    flight = elevation_ma + np.minimum(flight,cruise_alt*np.ones(len(flight)))[1:]
    flight = np.append(elevation[0]*np.ones(4),flight)
    flight = np.append(flight,elevation[0]*np.ones(4))
    
    flight_angle = np.arctan((flight[1:]-flight[:-1])/(1000*(dL/dX)))
    d_flight_angle_dx = (flight_angle[1:]-flight_angle[:-1])/(1000*(dL/dX))
    pitch_rate = V*d_flight_angle_dx 
    if plot:
        fig,ax = plt.subplots(3,1,sharex=True)
        ax[0].plot(1000*(dL/dX)*np.arange(len(elevation)),elevation,c="tab:brown")
        ax[0].fill_between(1000*(dL/dX)*np.arange(len(elevation)), elevation, np.zeros(len(elevation)),color="tab:brown")
        ax[0].plot(1000*(dL/dX)*np.arange(-4,len(elevation)+4,1),flight,c="green")
        ax[0].set_ylim(0,4000)
        ax[0].set_facecolor('skyblue')

        ax[1].plot(1000*(dL/dX)*np.arange(len(elevation)),flight[4:-4]-elevation)
        ax[1].set_ylabel("ground clearance (m)")
        ax[1].grid()

        ax[2].plot(1000*(dL/dX)*np.arange(len(pitch_rate)),(180/np.pi)*pitch_rate)
        ax[2].set_ylabel("pitch rate (deg/s)")
        ax[2].grid()
        plt.show()
