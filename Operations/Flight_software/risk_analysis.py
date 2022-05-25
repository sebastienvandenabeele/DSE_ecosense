import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats

def risk(location,topography,plot,dX,dY):

    def coordinate(lat,long):
        dx,dy = dX*(long-120),dY*(lat+30)
        return np.abs(dx),np.abs(dy)
    
    location = coordinate(location[0],location[1])

    value_range = 2200

    human_activity = pd.read_excel(r"./data/human_activity.xlsx")
    human_activity.set_index("loc",inplace=True)
    park_perimeter = pd.read_excel(r"./data/park_perimeter.xlsx")
    park_perimeter.set_index("loc",inplace=True)

    human_activity.lat,human_activity.long = coordinate(human_activity.lat,human_activity.long)
    park_perimeter.lat,park_perimeter.long = coordinate(park_perimeter.lat,park_perimeter.long)

    m1, m2 = human_activity.lat.values,human_activity.long.values
    xmin,xmax,ymin,ymax = m1.min(),m1.max(),m2.min(),m2.max()
    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([m1, m2])
    kernel = stats.gaussian_kde(values)
    Z = np.reshape(kernel(positions).T, X.shape)
    risk_score = (kernel(location)[0]-Z.min())/(Z.max()-Z.min())

    if plot:
        from matplotlib.colors import LinearSegmentedColormap
        colormap = LinearSegmentedColormap.from_list('italy', ['#008C45', '#0b914c', '#F4F5F0', '#cf2a32', '#CD212A'], N=value_range)
        from matplotlib.colors import ListedColormap
        background_color = np.array([1.0, 1.0, 1.0, 1.0])
        newcolors = colormap(np.linspace(0, 1, value_range))
        newcolors = np.vstack((newcolors, background_color))
        colormap = ListedColormap(newcolors)
        fig,ax = plt.subplots(1,2,facecolor='#FCF6F5FF',sharex=True,sharey=True,figsize=(15,9))
        c = ax[0].imshow(topography[0], cmap=colormap)
        c = ax[1].imshow(topography[0], cmap=colormap)
        
        ax[0].set_title("Activity map")
        ax[1].set_title("Risk map")
        ax[0].axis("off")
        ax[1].axis("off")
        
        ax[0].plot(park_perimeter.loc["Park","lat"].values,park_perimeter.loc["Park","long"].values,linewidth=4)
        ax[1].plot(park_perimeter.loc["Park","lat"].values,park_perimeter.loc["Park","long"].values,linewidth=4)
        
        ax[0].scatter(park_perimeter.loc["Launch site","lat"],park_perimeter.loc["Launch site","long"],s=200,label="Launch site",edgecolors = "k",zorder=5)
        ax[1].scatter(park_perimeter.loc["Launch site","lat"],park_perimeter.loc["Launch site","long"],s=200,label="Launch site",edgecolors = "k",zorder=5)
        
        human_activity.loc["Campsites"].plot.scatter(x="lat",y="long",ax=ax[0],color="yellow",label="Campsites")
        human_activity.loc["Hike trails"].plot.scatter(x="lat",y="long",ax=ax[0],color="purple",label="Hike trails")  
        human_activity.loc["Small towns"].plot.scatter(x="lat",y="long",ax=ax[0],color="red",label="Small settlements")   
        
        c = sns.kdeplot(x=human_activity["lat"].values,y=human_activity['long'].values,ax=ax[1],fill=True)

        ax[0].set_xlim(14100,15266)
        ax[0].set_ylim(2080,900)

        ax[0].scatter(location[0],location[1],zorder=5,s=200,edgecolors = "k",label="selected location")
        ax[1].scatter(location[0],location[1],zorder=5,s=200,edgecolors="k",label="selected location")

        ax[0].legend()
        ax[1].legend()

        plt.show()
    
    return risk_score

