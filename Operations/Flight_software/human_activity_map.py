from tracemalloc import start
import folium
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import atan2
import webbrowser

park_perimeter = pd.read_excel(r"./data/coordinates.xlsx")
park_perimeter.set_index("loc",inplace=True)
perimeter_points = park_perimeter.loc["Park"].values
perimeter_points = np.vstack((perimeter_points,perimeter_points[0,:]))
ground_station = list(park_perimeter.loc["Launch site"].values)
map = folium.Map(location = ground_station, tiles = "Stamen Terrain", zoom_start = 9)
tile = folium.PolyLine(perimeter_points, color="red", weight=2.5, opacity=1).add_to(map)

points = park_perimeter.drop(index=["Park"]).dropna().values
for point in points:
    folium.CircleMarker(list(point),radius=4).add_to(map)

map.save("park.html")
webbrowser.open_new_tab('park.html')
