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

#----------------------------------------------
#IMPORT DATA and SENSOR LOCATIONS
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
print("\nLocation coordinates :")
from area_selection import select_area_map
select_area = select_area_map(sensor_points,topography,dX,dY,dLat,dLon)

quit()
#location,distance = select_area_map(topography,True,dX,dY,dLat,dLong)
#print("\nFinal location: ",location)
#print("Distance from ground station: ",distance," km")
#input("Press Enter to continue...")

#------------------------------
#FLIGHT PATH
#------------------------------
from sensor_placement_strategy import SENSOR_PLACEMENT
ds = 1.5 #km subtile_spacing
location = [-33.62613184957613, 150.5]
sensor_df = SENSOR_PLACEMENT(location,topography,dLon,dLat,ds)

quit()

from flight_path_optimization import optimal_path
range_weight,cruise_alt = .75 , 300
for range_weight in [0.25,0.5,0.75]:
    path = optimal_path(sensor_df,dLat,dLon,range_weight,cruise_alt)
    route = sensor_df.iloc[path]
    print(route)
#------------------------------
#SELECTION OF AREA
#------------------------------
print("\nLocation coordinates :")
#from area_selection import select_area_map
#location,distance = select_area_map(topography,True,dX,dY,dLat,dLong)
#print("\nFinal location: ",location)
#print("Distance from ground station: ",distance," km")
#input("Press Enter to continue...")


#------------------------------
#RISK ANALYSIS OF AREA
#------------------------------
print("\nPerforming risk analysis...")
from risk_analysis import risk
risk_score = risk(location,topography,True,dX,dY,dLat,dLong,1.5)

if risk_score>0.66:
    spacing = 280
    risk_level = "High"
if risk_score>0.33 and risk_score<0.66:
    spacing = 500
    risk_level = "Medium"
if risk_score<0.33:
    spacing = 750
    risk_level = "Low"

print("risk level = "+risk_level)
print("sensor spacing = ",spacing," m")
input("Press Enter to continue...")

#from sensor_placement_strategy import sensor_placement_grid

#s = sensor_placement_grid(1)

#------------------------------
#SENSOR PLACEMENT
#------------------------------
print("\nPerforming sensor placement...")
from sensor_placement import sensor_locating
sensor_map,corner_points,sensor_points = sensor_locating(location,dX,dY,dLat,dLong,spacing)
#webbrowser.open_new_tab('sensor_locations.html')
print("check if sensors are placed correctly")
input("Press Enter to continue...")

#-------------------------------
#FLIGHT PATH
#-------------------------------
from flight_path import flight_map
print("\nPerforming flight planning...")
cruise_alt = 400    #m
cruise_spd = 60/3.6  #m/s
deployment_spd = 40/3.6 #m/s
wind_dir = -180
flight_map(True,location,topography,sensor_map,corner_points,sensor_points,spacing/1000,cruise_alt,cruise_spd,deployment_spd,wind_dir,dLat,dLong,dX,dY)
webbrowser.open_new_tab('flight_path.html')