from pickle import decode_long
import folium
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import atan2
import webbrowser
import random

def coordindate_reverse(x,y):
    lat,lon = (y/480) -30 , (x/480) +120
    return [lat,lon]

def coordinate(lat,long):
    dx,dy = 480*(long-120),480*(lat+30)
    return np.abs(dx),np.abs(dy)

def my_shuffle(array):
    random.shuffle(array)
    return array

def cost_function(path,df,dlat,dlon):
    ground_station = pd.DataFrame([-32.95281861307513,150.67634808302472,100]).transpose()
    ground_station.columns = ["lat","lon","elevation"]
    df_sel = df.loc[path,:]
    df_sel = pd.concat([ground_station,df_sel])
    df_sel = pd.concat([df_sel,ground_station])
    lat_diff,lon_diff = df_sel["lat"] - df_sel["lat"].shift() , df_sel["lon"] - df_sel["lon"].shift()
    y_diff,x_diff = lat_diff*dlat , lon_diff*dlon 
    R = np.sum(np.sqrt((x_diff**2 +  y_diff**2).dropna()))

    alt_std = np.std(df_sel.iloc[2:-1,:].values - df_sel.iloc[1:-2,:].values)
    return R,alt_std



def get_shortest_path_distance(points,origin, destination):
    """
    This function calculates the distance of the shortest path connecting
    origin and destination using A* search with distance heuristic.
    Args:
        world: carla world object
        planner: carla.macad_agents.navigation's Global route planner object
        origin (tuple): Origin (x, y, z) position on the map
        destination (tuple): Destination (x, y, z) position on the map

    Returns:
        The shortest distance from origin to destination along a feasible path

    """
    distance = 0.0
    for i in range(1, len(points)):
        l1 = points[i - 1][0].transform.location
        l2 = points[i][0].transform.location

        distance += math.sqrt((l1.x - l2.x) * (l1.x - l2.x) + (l1.y - l2.y) *
                              (l1.y - l2.y) + (l1.z - l2.z) * (l1.z - l2.z))
    return distance 





def SENSOR_PLACEMENT(location,topography,dlon,dlat,ds):
    mesh_df = pd.read_csv(r"../Sensor Reliability Simulation/data/custom_mesh.csv")
    min_lat,max_lat = mesh_df["lat"] - ds/(2*dlat) , mesh_df["lat"] + ds/(2*dlat)
    min_lon,max_lon = mesh_df["lon"] - ds/(2*dlon) , mesh_df["lon"] + ds/(2*dlon)
    mesh_df["min_lat"] = min_lat
    mesh_df["max_lat"] = max_lat
    mesh_df["min_lon"] = min_lon
    mesh_df["max_lon"] = max_lon
    mesh_df["lat_spacing"] = (mesh_df["spacing_req"].values/1000)/dlat
    mesh_df["lon_spacing"] = (mesh_df["spacing_req"].values/1000)/dlon

    sensor_points = np.empty(2)
    for subtile_index in range(len(mesh_df)):
        min_lat,max_lat,min_lon,max_lon,lat_spacing,lon_spacing = mesh_df.iloc[subtile_index,-6:]
        lat_range,lon_range = np.arange(min_lat,max_lat,lat_spacing),np.arange(min_lon,max_lon,lon_spacing)
        LAT,LON = np.meshgrid(lat_range,lon_range)
        subtile_grid = np.array([LAT.ravel(),LON.ravel()]).T
        sensor_points = np.vstack((sensor_points,subtile_grid))

    sensor_points = sensor_points[1:,:]
    dtile = 10 #km
    minlat,maxlat,minlon,maxlon = location[0]-dtile/(2*dlat), location[0]+dtile/(2*dlat), location[1]-dtile/(2*dlon), location[1]+dtile/(2*dlon)
    sensor_sel = sensor_points[(sensor_points[:,0]<maxlat)&(sensor_points[:,0]>minlat)&(sensor_points[:,1]<maxlon)&(sensor_points[:,1]>minlon)]
    sensor_df = pd.DataFrame(sensor_sel,columns=["lat","lon"])
    sensor_scaled_coordinates = coordinate(sensor_df["lat"].values,sensor_df["lon"].values)
    sensor_df["x"],sensor_df["y"] = sensor_scaled_coordinates[0], sensor_scaled_coordinates[1]
    sensor_df["elevation"] = topography[np.array(sensor_df["y"].values,dtype=int),np.array(sensor_df["x"].values,dtype=int)]
    print("random paths...")
    M = 10000
    random_paths = np.zeros((M,len(sensor_df)))
    paths_params = np.empty((M,2))
    for index in range(M):
        random_path = np.array(my_shuffle(np.arange(len(sensor_df))),dtype=int)
        random_paths[index] = random_path
        paths_params[index,:] = cost_function(random_path,sensor_df,dlat,dlon)
    
    fig,ax = plt.subplots(2,1)
    ax[0].hist(paths_params[:,0])
    ax[1].hist(paths_params[:,1])

    plt.show()



    random_paths = np.array(random_paths,dtype=int)
    print(random_paths)


    return sensor_df




    








