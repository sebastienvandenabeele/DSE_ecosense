import numpy as np
import pandas as pd
import simulation_functions as simfunc

df = pd.read_csv(r"./data/samples.csv")

df["MC"] = simfunc.MC(df["RH"].values, df["temp"].values)
df["FFDI"] = simfunc.FFDI(df["MC"].values, df["wind_spd"].values)
df["R"] = simfunc.R(df["FFDI"].values, 23.57)/3.6
df["LB"] = 1+10*(1-np.exp(-0.06*(1/3.6)*df["wind_spd"].values))
df = df[df.FFDI > 11]
df["wind_dir"] = 270-df["wind_dir"]

t_max = 10*60
N, M = 10000, len(df)
time = np.linspace(0, t_max, N)*np.ones((M, 1))
print(df)


def ellips_params(t, R, lb):
    l, w = R*t, l/lb
    c = np.sqrt((l/2)**2 - (w/2)**2)
    return np.array([l, w, c])


for index, t in enumerate(time):
    x_f, y_f = np.random.uniform(0, 100), np.random.uniform(0, 100)
    R, lb, wind_dir = df.iloc[index]["R"], df.iloc[index]["LB"], df.iloc[index]["wind_dir"]
    length, width, centre = ellips_params(t, R, lb)
    centre = [x_f+centre*np.cos(wind_dir*(np.pi/180))]
    #R, lb = df.iloc[index]["R"], df.iloc[index]["LB"]
    #l, w, c = ellips_params(t, R, lb)
