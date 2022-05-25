import numpy as np
import pandas as pd
import simulation_functions as simfunc
from matplotlib.patches import Ellipse, Polygon
import matplotlib.pyplot as plt
import scipy.interpolate as spinter
import matplotlib.animation as animation
import seaborn as sns
import mesh_types

df = pd.read_csv(r"./data/samples.csv")
df["wind_spd"] = df["wind_spd"]*0.2
df["MC"] = simfunc.MC(df["RH"].values, df["temp"].values)
df["FFDI"] = simfunc.FFDI(df["MC"].values, df["wind_spd"].values)
df["R"] = simfunc.R(df["FFDI"].values, 23.57)/3.6
df["LB"] = 1+10*(1-np.exp(-0.06*(1/3.6)*df["wind_spd"].values))
df = df[df.FFDI > 11]
df["wind_dir"] = 270-df["wind_dir"]
df = df[df.temp > 22]
df.index = np.arange(len(df))

t_max = 8*60
threshold = 0.05
N, M = 100, len(df)
size = 10000
mesh_points = mesh_types.mesh1(size, 250, 350)
time = np.linspace(0, t_max, N)*np.ones((M, 1))
C0_concentrations = np.array(
    [0, 0.85, 4.55, 6.75, 10.6, 14.25, 17.9, 23.3, 28.5, 31.2, 34.55, 39.1, 42.7, 48.2])
H2_concentrations = 0.1 * \
    np.array([0, 3, 4, 5, 5, 4, 4, 5, 5, 7, 15, 30, 40, 45])
time_concentrations = np.arange(0, 14, 1)

C0_concentration_function = spinter.interp1d(
    time_concentrations, C0_concentrations)
H2_concentration_function = spinter.interp1d(
    time_concentrations, H2_concentrations)


def initial_concentrations(t):
    return C0_concentration_function(t/60), H2_concentration_function(t/60)


run = True
if run:
    for index, t in enumerate(time):
        print(f"Running try no. {index+1}...")
        x_f, y_f = np.random.uniform(0, size, 2)
        R, lb, wind_dir, wind_spd, temp = df.iloc[index]["R"], df.iloc[index][
            "LB"], df.iloc[index]["wind_dir"], df.iloc[index]["wind_spd"], df.iloc[index]["temp"]
        length_ellipse, width_ellipse, centre_ellipse = simfunc.ellips_params(
            t, R, lb)
        length_triangle, width_triangle = simfunc.cone_params(
            t, wind_spd/3.6, lb)
        centre = [x_f+centre_ellipse*np.cos(np.deg2rad(wind_dir)),
                  y_f + centre_ellipse*np.sin(np.deg2rad(wind_dir))]

        x0, y0, radius = centre[0][0], centre[1][0], 500
        relevant_arg = np.argwhere(
            np.sqrt((mesh_points[:, 0]-x0)**2 + (mesh_points[:, 1]-y0)**2) < radius)
        relevant_points = mesh_points[relevant_arg][:, 0, :]

        upper_break = False
        for item in range(N):
            C0_init_ppm = initial_concentrations(t)[0]

            if upper_break:
                break

            detection_times = []
            for i, xy in enumerate(relevant_points):
                sensor_concentration_temp = simfunc.get_concentration(
                    (xy[0], xy[1]), (centre[0][i], centre[1][i]), wind_dir, item, width_triangle, t, C0_init_ppm)
                sensor_additional_time = item/N * t_max
                if sensor_concentration_temp > threshold and (sensor_additional_time+t[item]) < t_max:
                    sensor_reliability_value = np.random.uniform(0, 1)
                    if sensor_reliability_value <= 0.92:
                        detection_times.append(
                            sensor_additional_time+t[item])
            if len(detection_times) != 0:
                detection_time = np.min(detection_times)
                print(f"Fire Detected!!! in {detection_time} [s]")
                df.loc[index, "detection_time_gas"] = detection_time
                upper_break = True

            animation_plotting = False
            if animation_plotting:
                fig = plt.figure()

                def init():
                    sns.heatmap(np.zeros((10, 10)), vmax=.8,
                                square=True, cbar=False)

                def animate(i):
                    plt.clf()
                    x = np.linspace(
                        width_triangle[0], width_triangle[-1], len(t))
                    begin_N = 1
                    data = simfunc.concentration_distribution(x[begin_N:])
                    Z = np.array([C0_init_ppm[i+1]*simfunc.density_plot(x[begin_N:],
                                                                        params[0], params[1]) for params in data])
                    sns.heatmap(Z, vmin=0.0, vmax=0.05, cmap="Greys")

                anim = animation.FuncAnimation(
                    fig, animate, init_func=init, frames=N-1, interval=10, repeat=False)

                plt.show()

            plotting = False
            if plotting:
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.scatter(mesh_points[:, 0], mesh_points[:, 1])
                plt.scatter(x_f, y_f, color='red')
                plt.xlim(0, size)
                plt.ylim(0, size)
                plt.title(
                    f'Wind Direction: {np.round(wind_dir, 0)} [deg], Wind Speed: {np.round(wind_spd, 2)} [km/h], Temperature: {np.round(temp, 2)} [C]')
                plt.show()

    print("Saving to CSV...")
    df.to_csv(r"./data/fire_detection_time.csv")
