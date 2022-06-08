from tracemalloc import start
import folium
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import atan2

def nearest_point(x,arr):
    LSE = np.sum((arr-x)**2,axis=1)
    return arr[np.argwhere(LSE==np.min(LSE))][0][0]

def lat_long_to_scale(lat,long,dX,dY):
    dx,dy = dX*(long-120),dY*(lat+30)
    return [np.abs(dx),np.abs(dy)]

def moving_average(x, w):
    return np.convolve(x, np.ones(w), mode='same') / w

def forward_average(x,w):
    av = np.empty(len(x))
    for index,val in enumerate(x[w:-w]):
        av[index+w] = np.average(x[index:index+w])
    
    av[:w] = np.average(x[:w])
    av[-w:] = np.average(x[-w:])
    return av

def tops(x,w):
    av = np.empty(len(x))
    for index,val in enumerate(x[w:-w]):
        av[index+w] = np.max(x[index:index+w])

    av[:w] = np.max(x[:w])
    av[-w:] = np.max(x[-w:])
    return av    

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

def flight_map(plot,location,topography,map,outer_points,sensor_points,spacing,cruise_alt,cruise_spd,deployment_spd,wind_dir,dLat,dLong,dX,dY):
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
    climb_angle = np.deg2rad(10)
    climb_distance = (cruise_alt/np.tan(climb_angle))/1000 #km

    climb_point = [flight_path_points[0][0] + climb_distance*np.sin(np.deg2rad(wind_dir))/(dLat),
                    flight_path_points[0][1] + climb_distance*np.cos(np.deg2rad(wind_dir))/dLong]
    
    flight_path_points = np.vstack((flight_path_points[0],np.vstack((climb_point,flight_path_points[1:,:]))))

    flight_path_ = folium.PolyLine(flight_path_points, color="yellow", weight=2.5, opacity=1).add_to(map)
    map.save("flight_path.html")
    first_sensor,last_sensor = flight_path_points[2], flight_path_points[-2]

    lat,long = lat_long_to_scale(flight_path_points[:,0], flight_path_points[:,1],dX,dY)
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


    outbound_arg = np.argwhere(all_points[1:,:] == np.array([lat_long_to_scale(first_sensor[0],first_sensor[1],dX,dY)]))[0][0]
    inbound_arg = np.argwhere(all_points[1:,:] == np.array([lat_long_to_scale(last_sensor[0],last_sensor[1],dX,dY)]))[-1][0]

    #altitude path
    elevation_ma = forward_average(elevation,30)
    top = tops(elevation,10)
    top = np.maximum(moving_average(top,30),elevation[0])
    altitude = top + cruise_alt

    #heading path
    diff = all_points[1:] - all_points[:-1]
    diff[:,1] = -diff[:,1]
    arg = np.argwhere((diff[:,0] == 0.) & (diff[:,1]== 0.))
    diff[arg.flatten(),:] = diff[arg.flatten()-1,:]
    heading = np.rad2deg(np.array([atan2(dS[1],dS[0]) for dS in diff]))

    #velocity 
    velocity = deployment_spd*np.ones(len(altitude))
    N = 10
    velocity[N:outbound_arg] = cruise_spd
    velocity[inbound_arg+2:-N] = cruise_spd
    velocity[:N] = np.arange(N)*deployment_spd/(N-1)
    velocity[-N:] = deployment_spd - np.arange(N)*deployment_spd/((N)-1)

    #time itteration
    time = np.empty(len(velocity))
    ds = 1000*(dLat/dX)
    for index,speed in enumerate(velocity):
        if speed != 0.:
            dt = ds/speed
        else:
            dt = 0.
        time[index] = dt
    time = np.cumsum(time)

    #pitch rate
    flight_angle = np.append([0.],np.arctan((altitude[1:] - altitude[:-1])/ds))
    dtheta_dx = np.append([0.],flight_angle[1:]-flight_angle[:-1])/ds
    pitch_rate = np.rad2deg(dtheta_dx*velocity)

    #yaw rate
    dheading_dx = np.append([0.],heading[1:]-heading[:-1])/ds
    yaw_rate = dheading_dx*velocity

    print(np.shape(time))
    print(np.shape(all_points))
    print(np.shape(altitude))

    df = pd.DataFrame(time,columns=["time"])
    df["velocity"] = velocity
    df["altitude"] = altitude
    df["X"] = all_points[1:,0]
    df["Y"] = all_points[1:,1]
    df["heading"] = heading
    df["elevation"] = elevation
    df["pitch_rate"] = pitch_rate
    df.to_csv(r"./data/flight_path_data.csv",index=False)
    print(df)

    if plot:
        fig,ax = plt.subplots(4,1)
        ax[0].plot(1000*(dLat/dX)*np.arange(len(elevation)),altitude,c="tab:orange",label="flight path",linewidth = 2)
        ax[0].fill_between(1000*(dLat/dX)*np.arange(len(elevation)),np.zeros(len(elevation)),elevation,color = "tab:brown")
        ax[0].patch.set_facecolor('skyblue') 
        ax[0].patch.set_alpha(0.5)
        ax[0].set_ylim(0,5000)
        ax[0].set_ylabel("altitude [m]")
        ax[0].set_xlabel("ground distance [m]")

        ax[1].plot(time,velocity)
        ax[1].set_ylabel("velocity [m/s]")
        ax[1].set_xticks([])

        ax[2].plot(time,altitude-elevation)
        ax[2].set_ylabel("ground clearance [m]")
        ax[2].set_xlabel("time [s]")

        ax[3].plot(time,heading)
        ax[3].set_ylabel("heading [deg]")

        plt.legend()
        plt.show()
    