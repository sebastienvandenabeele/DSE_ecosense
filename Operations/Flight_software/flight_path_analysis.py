import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def path(sensor_df,topography):
    lon_points,lat_points = np.meshgrid(topography.columns.values,topography.index.values)
    positions = pd.DataFrame(np.vstack([lon_points.ravel(), lat_points.ravel()])).transpose()
    positions.columns = ["lon","lat"]
    positions["x"] = 480*(positions.lon.values-120)
    positions["y"] = -480*(positions.lat.values+30)
    sensor_df["x"] =  480*(sensor_df.lon.values-120)
    sensor_df["y"] =  -480*(sensor_df.lat.values+30)

    all_points = np.array([0,0])
    for index,coord in enumerate(sensor_df[["x","y"]].values):
        if index<len(sensor_df)-1:
            next_coord = sensor_df.iloc[index+1,:][["x","y"]]
            x_diff,y_diff = int(abs(next_coord[0]-coord[0])),int(abs(next_coord[1]-coord[1]))
            diff = np.maximum(x_diff,y_diff)
            x_range = np.linspace(coord[0],next_coord[0],diff)
            y_range = np.linspace(coord[1],next_coord[1],diff)
            inter_coords = np.hstack((x_range.reshape((diff,1)),y_range.reshape((diff,1))))
            all_points = np.vstack((all_points,inter_coords))
    
    all_points = all_points[1:,:]
    elevation = np.diag(topography.iloc[np.array(all_points[:,1],dtype=int)-np.min(np.array(all_points[:,1],dtype=int)),
                                np.array(all_points[:,0],dtype=int)-np.min(np.array(all_points[:,0],dtype=int))])
    
    all_points = np.vstack([(-all_points[:,1]/480) -30 , (all_points[:,0]/480) +120])
    points = pd.DataFrame(all_points).transpose()
    points.columns = ["lat","lon"]
    points["elev"] = elevation

    fig,ax = plt.subplots()
    c = ax.pcolormesh(lon_points,lat_points,topography.values,cmap="RdBu_r")
    ax.plot(points["lon"],points["lat"],c="k",linewidth=2)
    plt.colorbar(c)
    plt.show()
    
