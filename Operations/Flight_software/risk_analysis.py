from re import sub
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats
from matplotlib.path import Path
from shapely.geometry import Point, Polygon

def risk(topography,plot,dX,dY,dLat,dLong,dspacing):

    def coordinate(lat,long):
        dx,dy = dX*(long-120),dY*(lat+30)
        return np.abs(dx),np.abs(dy)
    
    def coordindate_reverse(x,y):
        lat,lon = -(y/dY) -30 , (x/dX) +120
        return [lat,lon]

    human_activity = pd.read_excel(r"./data/human_activity.xlsx")
    human_activity.set_index("loc",inplace=True)
    park_perimeter = pd.read_excel(r"./data/coordinates.xlsx")
    park_perimeter.set_index("loc",inplace=True)
    park_perimeter = park_perimeter.loc[["Park","Launch site"]]
    minLat,maxLat = park_perimeter.lat.min(),park_perimeter.lat.max()
    minLon,maxLon = park_perimeter.long.min(),park_perimeter.long.max()  

    human_activity.lat,human_activity.long = coordinate(human_activity.lat,human_activity.long)
    park_perimeter.lat,park_perimeter.long = coordinate(park_perimeter.lat,park_perimeter.long)
    park_perimeter = park_perimeter.loc["Park"]

    xmin,ymin = coordinate(minLat,minLon)
    xmax,ymax = coordinate(maxLat,maxLon)
    mpath = Path( np.vstack((park_perimeter.lat,-park_perimeter.long)).T ) 
    
    for spacing in [0.5,1,1.5,2.,4,6,8,10]:
        Nx,Ny = int(np.abs((xmax-xmin)*(dLong/dX)*(1/spacing))) , int(np.abs((ymax-ymin)*(dLat/dY)*(1/spacing)))
        X, Y = np.meshgrid(np.linspace(xmin,xmax,Nx),np.linspace(ymin,ymax,Ny))
        XY = np.dstack((X, -Y))
        XY = XY.reshape((-1, 2))
        mask = mpath.contains_points(XY).reshape(X.shape)
        arg = np.argwhere(mask==False)
        
    Nx,Ny = int(np.abs((xmax-xmin)*(dLong/dX)*(1/dspacing))) , int(np.abs((ymax-ymin)*(dLat/dY)*(1/dspacing)))
    m1, m2 = human_activity.lat.values,human_activity.long.values
    X, Y = np.meshgrid(np.linspace(xmin,xmax,Nx),np.linspace(ymin,ymax,Ny))
    XY = np.dstack((X, Y))
    XY = XY.reshape((-1, 2))

    mpath = Path( np.vstack((park_perimeter.lat,park_perimeter.long)).T ) 
    mask = mpath.contains_points(XY).reshape(X.shape)
    arg = np.argwhere(mask==False)

    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([m1, m2])
    kernel = stats.gaussian_kde(values)
    lightning_prob = 0.49
    Z = np.reshape(kernel(positions).T, X.shape)
    Z[arg[:,0],arg[:,1]] = 0.
    Z = Z/np.sum(Z)
    Z = lightning_prob/(np.size(Z)) +(1-lightning_prob)*Z
    Z[arg[:,0],arg[:,1]] = 0.
    Z = Z/np.sum(Z)
    subtile_df = pd.DataFrame({"fire_prob":Z.reshape(np.size(Z))})
    coordinates = coordindate_reverse(XY[:,0],XY[:,1])
    lat,lon = coordinates[0],coordinates[1]
    subtile_df["lat"] = lat
    subtile_df["lon"] = lon
    subtile_df["likelihood"] = (subtile_df["fire_prob"].values - subtile_df["fire_prob"].min())/(subtile_df["fire_prob"].max()-subtile_df["fire_prob"].min())
    subtile_df = subtile_df[subtile_df["fire_prob"]!=0.]
    subtile_df.to_csv("./data/prob_density.csv",index=False)
    if plot:
        from matplotlib.colors import LinearSegmentedColormap
        value_range = 2300
        colormap = LinearSegmentedColormap.from_list('italy', ['#008C45', '#0b914c', '#F4F5F0', '#cf2a32', '#CD212A'], N=value_range)
        from matplotlib.colors import ListedColormap
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        background_color = np.array([1.0, 1.0, 1.0, 1.0])
        newcolors = colormap(np.linspace(0, 1, value_range))
        newcolors = np.vstack((newcolors, background_color))
        colormap = ListedColormap(newcolors)
        fig,ax = plt.subplots(1,2,facecolor='#FCF6F5FF',sharex=True,sharey=True,figsize=(15,9))
        c = ax[0].imshow(topography, cmap=colormap)
        c = ax[1].imshow(topography, cmap=colormap)
        ax[0].set_title("Activity map")
        ax[1].set_title("Probability density map of fire ignition")
        ax[0].axis("off")
        ax[1].axis("off")
        from scipy.interpolate import interp1d
        ax[0].plot(park_perimeter.loc["Park","lat"].values,park_perimeter.loc["Park","long"].values,linewidth=4)
        ax[1].plot(park_perimeter.loc["Park","lat"].values,park_perimeter.loc["Park","long"].values,linewidth=4)

        ax[0].hlines(Y[:,0],xmin,xmax,linewidth=0.5,zorder=0.5,color="k")
        ax[0].vlines(X[0],ymin,ymax,linewidth=0.5,zorder=0.5,color="k")
        
        human_activity.loc["Campsites"].plot.scatter(x="lat",y="long",ax=ax[0],color="yellow",label="Campsites")
        human_activity.loc["Hike trails"].plot.scatter(x="lat",y="long",ax=ax[0],color="purple",label="Hike trails")  
        human_activity.loc["Small towns"].plot.scatter(x="lat",y="long",ax=ax[0],color="red",label="Small settlements")   

        cmap_Rd = plt.get_cmap('Reds')
        cmap_Rd.set_under('white',alpha=0)
        c = ax[1].pcolormesh(X, Y, Z, cmap=cmap_Rd, vmin=np.min(Z[Z!=0.]), vmax=np.max(Z))
        divider = make_axes_locatable(ax[1])
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(c, ax=ax[1],cax=cax)

        ax[0].set_xlim(14100,15266)
        ax[0].set_ylim(2080,900)

        ax[0].legend()
        ax[1].legend()

        ax[1].set_xlim(14100,15266)
        ax[1].set_ylim(2080,900)

        plt.show()
    