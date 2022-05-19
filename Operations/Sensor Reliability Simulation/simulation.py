import numpy as np
import pandas as pd
import simulation_functions as simfunc
from matplotlib.patches import Ellipse, Polygon
import matplotlib.pyplot as plt

df = pd.read_csv(r"./data/samples.csv")

df["MC"] = simfunc.MC(df["RH"].values, df["temp"].values)
df["FFDI"] = simfunc.FFDI(df["MC"].values, df["wind_spd"].values)
df["R"] = simfunc.R(df["FFDI"].values, 23.57)/3.6
df["LB"] = 1+10*(1-np.exp(-0.06*(1/3.6)*df["wind_spd"].values))
df = df[df.FFDI > 11]
df["wind_dir"] = 270-df["wind_dir"]

t_max = 8*60
N, M = 100, len(df)
size = 10000
x_spacing, y_spacing = 280, 280
x_sensor = np.arange(0, size+x_spacing, x_spacing)
y_sensor = np.arange(0, size+y_spacing, y_spacing)
X_sens, Y_sens = np.meshgrid(x_sensor, y_sensor)

time = np.linspace(0, t_max, N)*np.ones((M, 1))


def ellips_params(t, R, lb):
    l = R*t
    w = l/lb
    c = np.sqrt((l/2)**2 - (w/2)**2)
    return np.array([l, w, c])


def cone_params(t, u, lb):
    l = u*t
    w = l/lb
    return np.array([l, w])


for index, t in enumerate(time):
    if index < 1:
        x_f, y_f = np.random.uniform(0, size, 2)
        R, lb, wind_dir, wind_spd, temp = df.iloc[index]["R"], df.iloc[index][
            "LB"], df.iloc[index]["wind_dir"], df.iloc[index]["wind_spd"], df.iloc[index]["temp"]
        length, width, centre = ellips_params(t, R, lb)
        length_triangle, width_triangle = cone_params(t, wind_spd/3.6, lb)
        centre = [x_f+centre*np.cos(np.deg2rad(wind_dir)),
                  y_f + centre*np.sin(np.deg2rad(wind_dir))]

        ellipse_patches = [Ellipse(
            (centre[0][i], centre[1][i]), length[i], width[i], wind_dir, facecolor="none", edgecolor="orange", linewidth="0.2") for i in range(N)]

        length_triangle, width_triangle = cone_params(t, wind_spd, lb)
        print(np.shape(centre), np.shape(
            length_triangle), np.shape(width_triangle))

        fig, ax = plt.subplots(figsize=(9, 9))
        for i, ellipse in enumerate(ellipse_patches):
            ax.add_patch(ellipse)

        ax.scatter(X_sens, Y_sens)
        plt.scatter(x_f, y_f, color='red')
        plt.xlim(0, size)
        plt.ylim(0, size)
        plt.title(
            f'Wind Direction: {np.round(wind_dir, 0)} [deg], Wind Direction: {np.round(wind_spd, 2)} [km/h], Temperature: {np.round(temp, 2)} [C]')
        plt.show()

    #R, lb = df.iloc[index]["R"], df.iloc[index]["LB"]
    #l, w, c = ellips_params(t, R, lb)
