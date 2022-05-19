import folium
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


dX,dY = 480,480

loc0 = [-32.9719510,150.67942723]

def coordinate(x,y):
    long,lat = (x/dX)+120 , (-y/dY)-30
    return lat,long

def coordinate2(lat,long):
    dx,dy = dX*(long-120),dY*(lat+30)
    return np.abs(dx),np.abs(dy)

map = folium.Map(location = loc0, tiles = "Stamen Terrain", zoom_start = 9)
ground_station = folium.Marker(location=loc0, popup='Ground station').add_to(map)
dL = 40075/360 #km per degree of latitude/longitude
L = 10 

def nearest_point(x,arr):
    LSE = np.sum((arr-x)**2,axis=1)
    return arr[np.argwhere(LSE==np.min(LSE))][0][0]

def flight_path(start_point,DX,lat_or,lon_or):
    points = [start_point]
    lat,lon = start_point
    lon_dir = lon_or 
    for i in range(1+2*int(L/(DX*dL))):
        if i%2 == 0:
            lat, lon = lat, lon + lon_dir*L/dL
            lon_dir = -1*lon_dir
        
        else:
            lat, lon = lat+lat_or*DX , lon
        
        points.append([lat,lon])
    return np.array(points)

def sensor_placement(tile_loc,tile_risk):
    loc = coordinate(tile_loc[0], tile_loc[1])
    
    tile_points = np.array([[loc[0]-L/(2*dL),loc[1]+L/(2*dL)],
                            [loc[0]-L/(2*dL),loc[1]-L/(2*dL)],
                            [loc[0]+L/(2*dL),loc[1]-L/(2*dL)],
                            [loc[0]+L/(2*dL),loc[1]+L/(2*dL)],
                            [loc[0]-L/(2*dL),loc[1]+L/(2*dL)]])
    

    if tile_risk=="high":
        DX,DY = 0.28,0.28
    
    if tile_risk=="medium":
        DX,DY = 0.5,0.5
    
    if tile_risk=="low":
        DX,DY = 0.75,0.75
    
    Lat_range, Long_range = np.linspace(loc[1]-L/(2*dL),loc[1]+L/(2*dL),int(L/DX)), np.linspace(loc[0]-L/(2*dL),loc[0]+L/(2*dL),int(L/DY))
    dLat,dLon = np.abs(Lat_range[1]-Lat_range[0]) , np.abs(Long_range[1]-Long_range[0])
    X,Y = np.meshgrid(Lat_range,Long_range)
    
    removed_sensors = pd.read_excel(r"C:\Users\hidde\OneDrive\Bureaublad\DSE\removed_sensors.xlsx").values

    sensor_positions = np.vstack([X.ravel(), Y.ravel()])
    sensor_positions = np.delete(sensor_positions,removed_sensors.flatten(),axis=1)
    
    tile = folium.PolyLine(tile_points, color="red", weight=2.5, opacity=1).add_to(map)
    for index in range(len(sensor_positions[0])):
        location = [sensor_positions[1,index],sensor_positions[0,index]]
        folium.CircleMarker(location,popup='sensor: '+str(index),
                        radius=2,
                        weight=5).add_to(map)
    
    nearest_corner = nearest_point(loc0,tile_points)
    if nearest_corner[0]<loc0[0]:
        lat_or = -1
    else:
        lat_or = 1
    
    if nearest_corner[1]<loc0[1]:
        lon_or = -1
    else:
        lon_or = 1
    
    distance = 2*dL*np.sqrt(np.sum((nearest_corner-loc0)**2)) + int(L/DX)*L + (int(L/DX)-1)*DX
    flight_path_points = flight_path(nearest_corner,dLat,lat_or,lon_or)
    flight_path_points = np.vstack((loc0,flight_path_points))
    flight_path_points = np.vstack((flight_path_points,loc0))
    flight_path_ = folium.PolyLine(flight_path_points, color="yellow", weight=2.5, opacity=1).add_to(map)
    
    lat,long = coordinate2(flight_path_points[:,0], flight_path_points[:,1])
    coordinates = np.hstack((lat.reshape((len(lat),1)),long.reshape((len(long),1))))
    all_points = np.array([0,0])
    for index,coord in enumerate(coordinates):
        if index<len(coordinates)-1:
            next_coord = coordinates[index+1,:]
            x_diff,y_diff = int(abs(next_coord[0]-coord[0])),int(abs(next_coord[1]-coord[1]))
            diff = np.maximum(x_diff,y_diff)
            x_range = np.linspace(coord[0],next_coord[0],diff)
            y_range = np.linspace(coord[1],next_coord[1],diff)
            inter_coords = np.hstack((x_range.reshape((diff,1)),y_range.reshape((diff,1))))
            all_points = np.vstack((all_points,inter_coords))
    
    all_points = pd.DataFrame(all_points[1:,:],columns = ["X","Y"])
    all_points.to_excel("flight_path.xlsx",index=False)
    
            
tile_locs = np.array([[14574,1695]])
tile_risks = ["high","medium","low"]

for index,tile_loc in enumerate(tile_locs):
    tile_risk = tile_risks[index]
    sensor_placement(tile_loc, tile_risk)
    
map.save("mymap.html")