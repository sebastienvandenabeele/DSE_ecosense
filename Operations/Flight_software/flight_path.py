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
    return np.convolve(x, np.ones(w), mode='same') / w

flight_path_points = np.array(pd.read_excel(r"C:\Users\hidde\OneDrive\Bureaublad\DSE\flight_path.xlsx").values,dtype=int)

elevation = topography[flight_path_points[:,1],flight_path_points[:,0]]
elevation_ma = moving_average(elevation,10)

cruise_alt = 300    #m
V = 60/3.6          #m/s
flight = 1000*(dL/dX)*np.arange(len(elevation))
flight_angle = (10/180)*np.pi
top = np.arctan(flight_angle)*flight[int(len(elevation)/2)]
ac_flight = np.linspace(0,top,int(len(elevation)/2)+1)
desc_flight = np.linspace(top,0,int(len(elevation)/2))
ac_arg = np.argwhere(ac_flight>cruise_alt)[0][0]
desc_arg = np.argwhere(desc_flight<cruise_alt)[0][0]+len(ac_flight)
elevation_ma[:ac_arg] = elevation[0]
elevation_ma[desc_arg:] = elevation[-1]

flight = np.append(ac_flight,desc_flight)
flight = elevation_ma + np.minimum(flight,cruise_alt*np.ones(len(flight)))
flight = np.append(elevation[0]*np.ones(4),flight)
flight = np.append(flight,elevation[0]*np.ones(4))

flight_angle = np.arctan((flight[1:]-flight[:-1])/(1000*(dL/dX)))
d_flight_angle_dx = (flight_angle[1:]-flight_angle[:-1])/(1000*(dL/dX))
for dtheta in d_flight_angle_dx:
    print(dtheta)
pitch_rate = np.append([0.],V*d_flight_angle_dx)

fig,ax = plt.subplots(3,1,sharex=True)
ax[0].plot(1000*(dL/dX)*np.arange(len(elevation)),elevation,c="tab:brown")
ax[0].fill_between(1000*(dL/dX)*np.arange(len(elevation)), elevation, np.zeros(len(elevation)),color="tab:brown")
ax[0].plot(1000*(dL/dX)*np.arange(-4,len(elevation)+4,1),flight,c="green")
ax[0].set_ylim(0,10000)
ax[0].set_facecolor('skyblue')

ax[1].plot(1000*(dL/dX)*np.arange(len(elevation)),flight[4:-4]-elevation)
ax[1].set_ylabel("ground clearance (m)")
ax[1].grid()

ax[2].plot(1000*(dL/dX)*np.arange(len(pitch_rate)),(180/np.pi)*pitch_rate)
ax[2].set_ylabel("pitch rate (deg/s)")
ax[2].grid()
plt.show()