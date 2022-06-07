import geopandas as gpd
from shapely.geometry import mapping
import rasterio
from rasterio import mask as msk
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import MultiPolygon, Polygon

def topography_data():
    file = rasterio.open(r'./data/50S150E_20101117_gmted_mea075.tif')
    dataset = file.read() #(-50,120)->(-30,150)

    file2 = rasterio.open(r'./data/50S120E_20101117_gmted_mea075.tif')
    dataset2 = file2.read()

    dX,dY = np.shape(dataset[0])[1]/30,np.shape(dataset[0])[0]/20 #scale per degree of latitude/longitude
    dL = 40075.017/360 #km per degree of latitude/longitude
    dLat,dLong = dL*np.cos(np.deg2rad(33)),dL #km per degree of latitude/longitude

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


    return topography[0],dX,dY,dLat,dLong
