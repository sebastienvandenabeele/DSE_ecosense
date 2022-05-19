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


file = rasterio.open(r'C:\Users\hidde\Downloads\50S150E_20101117_gmted_mea075.tif')
dataset = file.read() #(-50,120)->(-30,150)

file2 = rasterio.open(r'C:\Users\hidde\Downloads\50S120E_20101117_gmted_mea075.tif')
dataset2 = file2.read()

dX,dY = np.shape(dataset[0])[1]/30,np.shape(dataset[0])[0]/20 #scale per degree of latitude/longitude
dL = 40075.017/360 #km per degree of latitude/longitude


def coordinate(lat,long):
    dx,dy = dX*(long-120),dY*(lat+30)
    return np.abs(dx),np.abs(dy)

coordinates = pd.read_excel(r"C:\Users\hidde\OneDrive\Bureaublad\DSE\coordinates.xlsx")
coordinates.set_index("loc",inplace=True)
coordinates.lat,coordinates.long = coordinate(coordinates.lat,coordinates.long)

path = r"C:\Users\hidde\Downloads\countries.geojson"
df = pd.read_json(path).iloc[:,1].values

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

value_range = 2200
topography1= clip_raster(file)
topography2 = clip_raster(file2)
topography = np.array([np.hstack((topography2[0],topography1[0]))])[0]

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

flight_path_points = np.array(pd.read_excel(r"C:\Users\hidde\OneDrive\Bureaublad\DSE\flight_path.xlsx").values,dtype=int)

elevation = topography[flight_path_points[:,1],flight_path_points[:,0]]
elevation_ma = moving_average(elevation,100)


cruise_alt = 300
flight = 1000*(dL/dX)*np.arange(len(elevation))
flight_angle = (20/180)*np.pi
top = np.arctan(flight_angle)*flight[int(len(elevation)/2)]
ac_flight = np.linspace(0,top,int(len(elevation)/2)+1)
desc_flight = np.linspace(top,0,int(len(elevation)/2))
flight = np.append(ac_flight,desc_flight)
flight = np.minimum(flight,cruise_alt*np.ones(len(flight)))
print(len(flight))
print(len(elevation))


fig = plt.figure(figsize=(18,5))
plt.plot(1000*(dL/dX)*np.arange(len(elevation)),elevation,c="tab:brown")
plt.fill_between(1000*(dL/dX)*np.arange(len(elevation)), elevation, np.zeros(len(elevation)),color="tab:brown")
plt.plot(1000*(dL/dX)*np.arange(len(elevation)),flight)
plt.ylim(0,10000)
plt.show()