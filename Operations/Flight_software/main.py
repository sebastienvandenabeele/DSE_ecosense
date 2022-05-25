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

location = np.array([-33.30695106292519, 150.28798863116293])
print("\nLocation coordinates :")
print("lat: ",location[0])
print("lon: ",location[1])

#----------------------------------------------
#IMPORT DATA
#----------------------------------------------
print("\nImporting terrain data...")
file = rasterio.open(r'./data/50S150E_20101117_gmted_mea075.tif')
dataset = file.read() #(-50,120)->(-30,150)

file2 = rasterio.open(r'./data/50S120E_20101117_gmted_mea075.tif')
dataset2 = file2.read()

dX,dY = np.shape(dataset[0])[1]/30,np.shape(dataset[0])[0]/20 #scale per degree of latitude/longitude
dL = 40075.017/360 #km per degree of latitude/longitude
dLat,dLong = dL*np.cos(np.deg2rad(location[0])),dL 

def coordinate(lat,long):
    dx,dy = dX*(long-120),dY*(lat+30)
    return np.abs(dx),np.abs(dy)

df = pd.read_json(r"./data/countries.geojson").iloc[:,1].values

def country_select(country):
    for i in df:
        if i["properties"]["ADMIN"]==country:
            return pd.DataFrame(i)
        
country = "Australia" 
AUS = country_select(country).iloc[-1,-1]

polygons = []
for polygon in AUS:
    polygon = Polygon(polygon[0])
    polygons.append(polygon)

geom = MultiPolygon(polygons)
clipped_array, clipped_transform = msk.mask(file, [mapping(geom)], crop=True)

def clip_raster(img):
     clipped_array, clipped_transform = msk.mask(img, [geom], crop=True)
     clipped_array, clipped_transform = msk.mask(img, [geom],
                                                           crop=True, nodata=2300)
     return clipped_array

topography1= clip_raster(file)
topography2 = clip_raster(file2)
topography = np.array([np.hstack((topography2[0],topography1[0]))])

topography_data = pd.DataFrame(topography[0])
topography_data.to_csv("./data/topography.csv")


#------------------------------
#RISK ANALYSIS OF AREA
#------------------------------
print("\nPerforming risk analysis...")
from risk_analysis import risk
risk_score = risk(location,topography,False,dX,dY)
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

#------------------------------
#SENSOR PLACEMENT
#------------------------------
print("\nPerforming sensor placement...")
from sensor_placement import sensor_locating
sensor_map,corner_points,sensor_points = sensor_locating(location,dX,dY,dLat,dLong,spacing)
webbrowser.open_new_tab('sensor_locations.html')
print("check if sensors are placed correctly, press enter to continue")

#-------------------------------
#FLIGHT MAP
#-------------------------------
from flight_path import flight_analysis, flight_map, flight_analysis
print("\nPerforming flight planning...")
map,flight_points = flight_map(location,sensor_map,corner_points,sensor_points,spacing/1000)
webbrowser.open_new_tab('flight_path.html')
cruise_alt = 300    #m
V = 60/3.6          #m/s
flight_analysis(flight_points,topography[0],dX,dY,dL,cruise_alt,V,True)

