import numpy as np
import pandas as pd
from matplotlib.path import Path
import folium
import webbrowser

def coordinate(lat,lon,dX,dY):
    dx,dy = dX*(lon-120),dY*(lat+30)
    return np.abs(dx),np.abs(dy)

def reverse_coordinate(x,y,dX,dY):
    lat,lon = -(y/dY) -30 , (x/dX) +120
    return lat,lon

def select_area_map(sensor_points,showmap,dLat,dLon,Nbr):
    N_flights = int(len(sensor_points)/Nbr)
    value_range = 2200
    park_perimeter = pd.read_excel(r"./data/coordinates.xlsx")
    park_perimeter.set_index("loc",inplace=True)
    ground_station = park_perimeter.loc["Launch site"].values
    ymin,ymax = park_perimeter.loc["Park","lat"].min(),park_perimeter.loc["Park","lat"].max()
    xmin,xmax = park_perimeter.loc["Park","long"].min(),park_perimeter.loc["Park","long"].max()  
    Nx,Ny = int(np.abs((xmax-xmin)*(dLon)*(1/10))) , int(np.abs((ymax-ymin)*(dLat)*(1/10)))
    X, Y = np.meshgrid(np.linspace(xmin,xmax,Nx),np.linspace(ymin,ymax,Ny))
    XY = np.dstack((X, Y))
    XY = XY.reshape((-1, 2))
    mpath = Path( np.vstack((park_perimeter.loc["Park","long"],park_perimeter.loc["Park","lat"])).T ) 
    mask = mpath.contains_points(XY)
    XY = XY[mask]
    XY = XY[:,[1,0]]

    map = folium.Map(location = (ground_station[0],ground_station[1]), tiles = "Stamen Terrain", zoom_start = 9,tooltip = 'This tooltip will appear on hover')
    g_s = folium.Marker(location=(ground_station[0],ground_station[1]), popup='Ground station').add_to(map)
    tile = folium.PolyLine(park_perimeter.loc["Park",["lat","long"]].values, color="red", weight=1, opacity=1,linewidth =2).add_to(map)
    tiles = []
    for index,tile_loc in enumerate(XY):
        lat_loc,lon_loc = tile_loc
        tile_vert = np.array([[lat_loc + (10/2)/dLat,lon_loc + (10/2)/dLon],
                            [lat_loc + (10/2)/dLat,lon_loc - (10/2)/dLon],
                            [lat_loc - (10/2)/dLat,lon_loc - (10/2)/dLon],
                            [lat_loc - (10/2)/dLat,lon_loc + (10/2)/dLon],
                            [lat_loc + (10/2)/dLat,lon_loc + (10/2)/dLon]])
        
        tile = folium.PolyLine(tile_vert, color="black", weight=2.5, opacity=1).add_to(map)
        path = folium.PolyLine(np.array([ground_station,tile_loc]), color="blue", weight=2.5, opacity=1).add_to(map)
        tiles.append(tile_vert)

    map.save("area_selection.html")
    if showmap:
        webbrowser.open_new_tab('area_selection.html')
    
    return tiles

    


            
        
        
        
