from pickle import decode_long
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib

def select_area_map(sensor_points,topography,dX,dY,dLat,dLon):

    def coordinate(lat,lon):
        dx,dy = dX*(lon-120),dY*(lat+30)
        return np.abs(dx),np.abs(dy)
    
    def reverse_coordinate(x,y):
        lat,lon = -(y/dY) -30 , (x/dX) +120
        return lat,lon
    
    value_range = 2200
    park_perimeter = pd.read_excel(r"./data/coordinates.xlsx")
    park_perimeter.set_index("loc",inplace=True)
    ground_station = park_perimeter.loc["Launch site"].values
    plt.scatter(sensor_points[:,1],sensor_points[:,0],c="k",s=1)
    plt.plot(park_perimeter.loc["Park"].long.values,park_perimeter.loc["Park"].lat.values)
    plt.show()


    park_perimeter.long,park_perimeter.lat = coordinate(park_perimeter.lat,park_perimeter.long)
 
    from matplotlib.colors import LinearSegmentedColormap
    colormap = LinearSegmentedColormap.from_list('italy', ['#008C45', '#0b914c', '#F4F5F0', '#cf2a32', '#CD212A'], N=value_range)
    from matplotlib.colors import ListedColormap
    background_color = np.array([1.0, 1.0, 1.0, 1.0])
    newcolors = colormap(np.linspace(0, 1, value_range))
    newcolors = np.vstack((newcolors, background_color))
    colormap = ListedColormap(newcolors)
    range = matplotlib.patches.Ellipse((park_perimeter.loc["Launch site","long"],park_perimeter.loc["Launch site","lat"]), 2*100*dX/dLon, 2*100*dX/dLat,  color='b', fill=False,label="100km radius")

    fig,ax = plt.subplots(facecolor='#FCF6F5FF',sharex=True,sharey=True,figsize=(15,9))
    c = ax.imshow(topography, cmap=colormap)
    ax.plot(park_perimeter.loc["Park","long"].values,park_perimeter.loc["Park","lat"].values,linewidth=4,color = "tab:orange",label="park perimeter")
    ax.scatter(park_perimeter.loc["Launch site","long"],park_perimeter.loc["Launch site","lat"],s=200,label="Launch site",edgecolors = "k",zorder=5)
    ax.set_title("Activity map")
    ax.add_patch(range)
    ax.axis("off")
    ax.set_ylim(park_perimeter.loc["Launch site","lat"] + 1.5*100*dX/dLat, park_perimeter.loc["Launch site","lat"] - 1.5*100*dX/dLat  )
    ax.set_xlim(park_perimeter.loc["Launch site","long"] - 1.5*100*dX/dLat, park_perimeter.loc["Launch site","long"] + 1.5*100*dX/dLat  )
    sensor_points = coordinate(sensor_points[:,0],sensor_points[:,1])
    print(sensor_points)
    ax.scatter(sensor_points[0],sensor_points[1],color="k",s = 1,label="sensors")

    coords = []

    def onclick(event):
        ix, iy = event.xdata, event.ydata
        iy, ix = reverse_coordinate(ix,iy)
        print("\nlat: ",iy)
        print("lon: ",ix)
        coords.append((iy, ix))
        return coords

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    location = list(coords[0])
    distance = np.abs(location-ground_station)
    distance[0],distance[1] = distance[0]*dLat , distance[1]*dLong 
    distance = np.sqrt(np.sum(distance**2))
    return location,distance