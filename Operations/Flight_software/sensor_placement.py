import folium
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def sensor_locating(location,dX,dY,dLat,dLong,spacing):
    spacing = spacing/1000
    def deg_to_scale(lat,long):
        dx,dy = dX*(long-120),dY*(lat+30)
        return np.abs(dx),np.abs(dy)
    
    def scale_to_deg(x,y):
        long,lat = (x/dX)+120 , (-y/dY)-30
        return lat,long

    park_perimeter = pd.read_excel(r"./data/park_perimeter.xlsx")
    park_perimeter.set_index("loc",inplace=True)
    ground_station = list(park_perimeter.loc["Launch site"].values)
    map = folium.Map(location = ground_station, tiles = "Stamen Terrain", zoom_start = 9)
    ground_station = folium.Marker(location=ground_station, popup='Ground station').add_to(map)

    L = 10 #km
    outer_points = np.array([[location[0]+(L/2)/dLat,location[1]+(L/2)/dLong],
                            [location[0]+(L/2)/dLat,location[1]-(L/2)/dLong],
                            [location[0]-(L/2)/dLat,location[1]-(L/2)/dLong],
                            [location[0]-(L/2)/dLat,location[1]+(L/2)/dLong],
                            [location[0]+(L/2)/dLat,location[1]+(L/2)/dLong]])
    
    lat_range = np.linspace(np.min(outer_points[:,0]),np.max(outer_points[:,0]),int(L/spacing))
    lon_range = np.linspace(np.min(outer_points[:,1]),np.max(outer_points[:,1]),int(L/spacing))
    X,Y = np.meshgrid(lat_range,lon_range)
    sensor_positions = np.vstack([X.ravel(), Y.ravel()])

    removed_sensors = pd.read_excel(r"./data/removed_sensors.xlsx")
    if len(removed_sensors)>0:
        sensor_positions = np.delete(sensor_positions,removed_sensors.flatten(),axis=1)
    tile = folium.PolyLine(outer_points, color="red", weight=2.5, opacity=1).add_to(map)

    for index in range(len(sensor_positions[0])):
        location = [sensor_positions[0,index],sensor_positions[1,index]]

        folium.CircleMarker(location,popup='sensor: '+str(index),
                        radius=2,
                        weight=5).add_to(map)
    
    map.save("sensor_locations.html")
    return map,outer_points,sensor_positions