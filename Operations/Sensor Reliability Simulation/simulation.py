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
df = df[df.temp > 22]
df.index = np.arange(len(df))
print(df)

t_max = 8*60
N, M = 100, len(df)
size = 10000
x_spacing, y_spacing = 280, 280
x_sensor = np.arange(0, size+x_spacing, x_spacing)
y_sensor = np.arange(0, size+y_spacing, y_spacing)
mesh_points = np.vstack(
    map(np.ravel, np.meshgrid(x_sensor, y_sensor))).transpose()

time = np.linspace(0, t_max, N)*np.ones((M, 1))


def detection_time(patch, points):
    arg = np.array([patch.contains_point(point) for point in points])
    if any(arg) == True:
        return True
    else:
        return False


for index, t in enumerate(time):
    print(f"Running try no. {index+1}")
    x_f, y_f = np.random.uniform(0, size, 2)
    R, lb, wind_dir, wind_spd, temp = df.iloc[index]["R"], df.iloc[index][
        "LB"], df.iloc[index]["wind_dir"], df.iloc[index]["wind_spd"], df.iloc[index]["temp"]
    length, width, centre = simfunc.ellips_params(t, R, lb)
    length_triangle, width_triangle = simfunc.cone_params(
        t, wind_spd/3.6, lb)
    centre = [x_f+centre*np.cos(np.deg2rad(wind_dir)),
              y_f + centre*np.sin(np.deg2rad(wind_dir))]

    for i in range(N):

        ellipse_patches = Ellipse((centre[0][i], centre[1][i]), length[i], width[i],
                                  wind_dir, facecolor="none", edgecolor="orange", linewidth="0.2")

        triangle_points = simfunc.triangle_points(
            length_triangle, width_triangle, centre, wind_dir, i)

        triangle_patches = Polygon(
            triangle_points, closed=True, facecolor="none", edgecolor="grey", linewidth="0.2")

        detection_gas = detection_time(triangle_patches, mesh_points)
        if detection_gas == True:
            detection_time_gas = time[0][i]
            df.loc[index, "detection_time_gas"] = detection_time_gas
            break

    #
    # try:
    #    detection = time[0][np.argwhere(np.array(detection) == True)[0][0]]
    # except:
    #    detection = np.nan

    #df.loc[index, "detection_time"] = detection

    plotting = False
    if plotting:
        fig, ax = plt.subplots(figsize=(8, 8))
        for i, ellipse in enumerate(ellipse_patches):
            ax.add_patch(ellipse)
            ax.add_patch(triangle_patches[i])
        ax.scatter(mesh_points[:, 0], mesh_points[:, 1])
        plt.scatter(x_f, y_f, color='red')
        plt.xlim(0, size)
        plt.ylim(0, size)
        plt.title(
            f'Wind Direction: {np.round(wind_dir, 0)} [deg], Wind Direction: {np.round(wind_spd, 2)} [km/h], Temperature: {np.round(temp, 2)} [C]')
        plt.show()

print(df)
