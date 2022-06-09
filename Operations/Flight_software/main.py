import geopandas as gpd
from shapely.geometry import mapping
import rasterio
from rasterio import mask as msk
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import MultiPolygon, Polygon
import seaborn as sns
from sklearn.neighbors import KernelDensity
import webbrowser
from matplotlib.path import Path
import math

#----------------------------------------------
#IMPORT DATA and ALL SENSOR LOCATIONS
#----------------------------------------------
print("\nImporting data...")
from terrain_analysis import topography_data
from sensor_placement_strategy import SENSOR_PLACEMENT
#dX,dY: scale/deg of lat or lon , dLat,dLong: km per degree of lat/lon
topography,dX,dY,dLat,dLon = topography_data()
ds = 1.5 #km subtile_spacing
sensor_points = SENSOR_PLACEMENT(dLon,dLat,ds)

#------------------------------
#SELECTION OF AREA
#------------------------------
print("\nSelecting location...")
from area_selection import select_area_map
Number_Sensors_per_Flight = 550
flights = select_area_map(sensor_points,False,dLat,dLon,Number_Sensors_per_Flight)
selected_tile_nbr = 0
tile = flights[selected_tile_nbr]
mpath = Path( tile ) 
mask = mpath.contains_points(sensor_points)
sensor_points = sensor_points[mask]
sensor_df = pd.DataFrame(sensor_points,columns = ["lat","lon"])
N_sens = len(sensor_points)
print("\nNumber of sensors in selected location:",N_sens)
if N_sens>Number_Sensors_per_Flight:
    N_flight = math.ceil(N_sens/Number_Sensors_per_Flight)
else:
    N_flight = 1
print("\nNumber of flights needed for selected location:",N_flight)

#------------------------------
#FLIGHT PATH
#------------------------------
from flight_path_optimization import optimal_path
from flight_path_analysis import path

range_weight = 0.9
cruise_alt = 200 #m
cruise_spd,mvr_spd = 70/3.6 , 40/3.6

if N_flight>1:
    for flight_nbr in range(N_flight):
        start,stop = int(flight_nbr*len(sensor_df)/N_flight), int((flight_nbr+1)*len(sensor_df)/N_flight)
        sensor_df = sensor_df.iloc[start:stop,:]
        x,y = np.array(480*(sensor_df.lon.values-120),dtype=int),np.array(-480*(sensor_df.lat.values+30),dtype=int)
        elevation = topography[y,x]
        sensor_df["elevation"] = elevation
        optimal_route = optimal_path(sensor_df,dLat,dLon,range_weight,cruise_alt)
        sensor_df = sensor_df.loc[optimal_route,:]
        print(sensor_df)

       # X,Y = np.arange(np.min(x),np.max(x)+1,1), np.arange(np.min(y),np.max(y)+1,1)
       # lat,lon = (-Y/480) -30 , (X/480) +120
       # Z = topography[np.min(y):(np.max(y)+1),np.min(x):(np.max(x)+1)]
       # topography_df = pd.DataFrame(Z,columns=lon,index=lat)
       # flight_path = path(sensor_df,topography_df)

       # fig,ax = plt.subplots()
       # c = ax.pcolormesh(lon,lat,Z,cmap="RdBu_r")
       # ax.scatter(sensor_df.lon,sensor_df.lat,zorder=3,color="k")
       # ax.plot(sensor_df.lon,sensor_df.lat,color="k")
       # plt.colorbar(c)
       # plt.show()
       # break