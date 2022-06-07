import numpy as np
import pandas as pd

def coordindate_reverse(x,y):
    lat,lon = (y/480) -30 , (x/480) +120
    return [lat,lon]

def coordinate(lat,long):
    dx,dy = 480*(long-120),480*(lat+30)
    return np.abs(dx),np.abs(dy)

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
    print(len(sensor_points))
    dtile = 10 #km
    minlat,maxlat,minlon,maxlon = location[0]-dtile/(2*dlat), location[0]+dtile/(2*dlat), location[1]-dtile/(2*dlon), location[1]+dtile/(2*dlon)
    sensor_sel = sensor_points[(sensor_points[:,0]<maxlat)&(sensor_points[:,0]>minlat)&(sensor_points[:,1]<maxlon)&(sensor_points[:,1]>minlon)]
    sensor_df = pd.DataFrame(sensor_sel,columns=["lat","lon"])
    sensor_scaled_coordinates = coordinate(sensor_df["lat"].values,sensor_df["lon"].values)
    sensor_df["x"],sensor_df["y"] = sensor_scaled_coordinates[0], sensor_scaled_coordinates[1]
    sensor_df["elevation"] = topography[np.array(sensor_df["y"].values,dtype=int),np.array(sensor_df["x"].values,dtype=int)]
    return sensor_df




    








