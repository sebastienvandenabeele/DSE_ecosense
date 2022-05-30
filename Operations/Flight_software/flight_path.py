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

def flight_map(plot,location,topography,map,outer_points,sensor_points,spacing,cruise_alt,cruise_spd,wind_dir,dL,dX,dY):
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

    climb_point = [flight_path_points[0][0] + climb_distance*np.sin(np.deg2rad(wind_dir))/(dL*np.cos(np.deg2rad(30))),
                    flight_path_points[0][1] + climb_distance*np.cos(np.deg2rad(wind_dir))/dL]
    
    flight_path_points = np.vstack((flight_path_points[0],np.vstack((climb_point,flight_path_points[1:,:]))))

    flight_path_ = folium.PolyLine(flight_path_points, color="yellow", weight=2.5, opacity=1).add_to(map)
    map.save("flight_path.html")

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
    elevation_ma = moving_average(elevation,80)

    #altitude path
    flight = 1000*(dL/dX)*np.arange(len(elevation))
    climb_angle = (10/180)*np.pi
    flight[:int(len(flight)/2)] = np.arctan(climb_angle)*flight[:int(len(flight)/2)]
    flight[int(len(flight)/2):] = flight[int(len(flight)/2)-1] - np.arctan(climb_angle)*(flight[int(len(flight)/2):]-flight[int(len(flight)/2)])
    flight = np.minimum(flight,cruise_alt*np.ones(len(flight)))
    altitude = flight + np.maximum(elevation_ma,elevation[0]*np.ones(len(flight)))

    #velocity path
    velocity = np.minimum(flight,cruise_spd)
    time = np.arange(len(flight)-2)/ (velocity[1:-1])
    time = np.append([0.],np.append(time,time[-1]+time[1]-time[0]))

    #heading path
    diff = all_points[1:] - all_points[:-1]
    diff[:,1] = -diff[:,1]
    arg = np.argwhere((diff[:,0] == 0.) & (diff[:,1]== 0.))
    diff[arg.flatten(),:] = diff[arg.flatten()-1,:]
    heading = np.rad2deg(np.array([atan2(dS[1],dS[0]) for dS in diff]))

    if plot:
        fig,ax = plt.subplots()
        ax.plot(np.arange(len(flight)),altitude,c="tab:orange",label="flight path",linewidth = 2)
        ax.fill_between(np.arange(len(flight)),np.zeros(len(flight)),elevation,color = "tab:brown")
        ax.patch.set_facecolor('skyblue') 
        ax.patch.set_alpha(0.5)
        ax.set_ylim(0,5000)
        plt.legend()

        fig,ax = plt.subplots(4,1)
        ax[0].plot(time,velocity)
        ax[0].set_ylabel("velocity")

        ax[1].plot(time,altitude-elevation)
        ax[1].set_ylabel("ground clearance")

        ax[2].plot(time,heading)
        ax[2].set_ylabel("heading")

        plt.legend()
        plt.show()
    