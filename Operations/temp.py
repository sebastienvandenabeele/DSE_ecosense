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
topography = np.array([np.hstack((topography2[0],topography1[0]))])

save = False
if save==True:
    topography_df = pd.DataFrame(topography[0])
    topography_df.to_csv("topography.csv",index=False)

plot=True
if plot==True:    
    from matplotlib.colors import LinearSegmentedColormap
    italy_colormap = LinearSegmentedColormap.from_list('italy', ['#008C45', '#0b914c', '#F4F5F0', '#cf2a32', '#CD212A'], N=value_range)
    from matplotlib.colors import ListedColormap
    background_color = np.array([0.9882352941176471, 0.9647058823529412, 0.9607843137254902, 1.0])
    newcolors = italy_colormap(np.linspace(0, 1, value_range))
    newcolors = np.vstack((newcolors, background_color))
    italy_colormap = ListedColormap(newcolors)
    
    fig,ax = plt.subplots(1,2,facecolor='#FCF6F5FF',sharex=True,sharey=True,figsize=(15,9))
    c = ax[0].imshow(topography[0], cmap=italy_colormap)
    c = ax[1].imshow(topography[0], cmap=italy_colormap)
    
    ax[0].set_title("Activity map")
    ax[1].set_title("Risk map")
    ax[0].axis("off")
    ax[1].axis("off")
    
    ax[0].plot(coordinates.loc["Park","lat"].values,coordinates.loc["Park","long"].values,linewidth=4)
    ax[1].plot(coordinates.loc["Park","lat"].values,coordinates.loc["Park","long"].values,linewidth=4)
    
    ax[0].scatter(coordinates.loc["Launch site","lat"],coordinates.loc["Launch site","long"],s=200,label="Launch site")
    ax[1].scatter(coordinates.loc["Launch site","lat"],coordinates.loc["Launch site","long"],s=200,label="Launch site",zorder=5)
    
    coordinates.loc["Campsites"].plot.scatter(x="lat",y="long",ax=ax[0],color="yellow",label="Campsites")
    coordinates.loc["Hike trails"].plot.scatter(x="lat",y="long",ax=ax[0],color="purple",label="Hike trails")  
    coordinates.loc["Small towns"].plot.scatter(x="lat",y="long",ax=ax[0],color="red",label="Small settlements")   
    
    c = sns.kdeplot(x=coordinates["lat"].values,y=coordinates['long'].values,ax=ax[1],fill=True)
    
    ax[0].set_xlim(14100,15266)
    ax[0].set_ylim(2080,900)
    ax[0].legend()
    ax[1].legend()