import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from scipy import stats

data = pd.read_excel(r"C:\Users\hidde\OneDrive\Bureaublad\DSE\temperature_data.xlsx")
wind_directions = ["N","NNE","NE","ENE","E","ESE", "SE","SSE","S","SSW","SW","WSW", "W","WNW","NW","NNW","N"]
wind_angles = [22.5*s for s in range(len(wind_directions))]
wind_directions,wind_angles = wind_directions[1:],wind_angles[1:]
wind_zip = zip(wind_directions,wind_angles)
wind_dir = dict(wind_zip)
data["wind_dir"] = np.array([wind_dir[direction] for direction in data["wind_dir"].values])
wind_directions = ["land wind","sea wind"]
data["wind_dir"] = np.array([0 if 180<=direction<=360 else 1 for direction in data["wind_dir"].values])
data["wind direction"] = ["land" if direction==0 else "sea" for direction in data["wind_dir"].values]
print(data.corr())

fire_counts = pd.read_csv(r"C:\Users\hidde\OneDrive\Bureaublad\DSE\fire_counts_NSW.csv").dropna(axis=1)
fire_counts['Date'] = pd.to_datetime(fire_counts['DOY'], format='%j').dt.strftime('%m')
fire_counts.set_index("Date",inplace=True)
fire_counts = fire_counts.drop(columns=["DOY"])
fire_counts = fire_counts - fire_counts.shift()
fire_counts = fire_counts.groupby("Date").sum()
fire_stat = pd.DataFrame([])

for col in fire_counts.columns.values:
    fire_stat[col] = (fire_counts[col]-fire_counts.mean(axis=1))/(fire_counts.std(axis=1))

fire_stat = fire_stat[fire_stat.abs()<3]

for col in fire_counts.columns.values:
    fire_stat[col] = fire_stat[col]*fire_counts.std(axis=1)+fire_counts.mean(axis=1)

fire_stat = fire_stat.mean(axis=1)

sel_months = ["dec","jan","feb"]
data = data[data.month.isin(sel_months)]
df = data[["max_temp","RH","wind_spd"]]
df = df[df.RH<=80]

def MC(RH,T):
    return 5.658+0.04651*RH+(0.0003151*(RH**3)/T)-0.184*(T**0.77)

def FFDI(MC,U):
    return (34.81*np.exp(0.987*np.log(10))*(MC)**(-2.1))*(np.exp(0.0234*U))

def R(ffdi,w):
    return 0.0012*ffdi*w

df["MC"] = MC(df["RH"].values,df["max_temp"].values)
df["FFDI"] = FFDI(df["MC"].values,df["wind_spd"].values)
df["R"] = R(df["FFDI"].values,23.57)/3.6
df["LB"] = 1+10*(1-np.exp(-0.06*(1/3.6)*df["wind_spd"].values))

t_max = 10*60
N,M = 10000,len(df)
time = np.linspace(0,t_max,N)*np.ones((M,1))

def ellips_params(t,R,LB):
    l = R*t
    w = l/LB
    return np.array([l,w])

for index,t in enumerate(time):
    R,LB = df.iloc[index]["R"],df.iloc[index]["LB"]
    l,w = ellips_params(t, R, LB)
    



plot = False
if plot:
    fig,ax = plt.subplots()
    
    fire_stat.plot(ax=ax,linewidth=5,zorder=5,label="moving average")
    fire_counts.plot.bar(ax=ax)
    plt.legend()
    
    fig,ax = plt.subplots(3,1,figsize=(10,10))
    seaborn.scatterplot(ax = ax[0], data = data, x="max_temp",y="RH",hue="wind direction")
    seaborn.scatterplot(ax = ax[1], data = data, x="max_temp",y="RH",hue="month")
    seaborn.scatterplot(ax = ax[2], data = data, x="max_temp",y="RH",hue="wind_spd")