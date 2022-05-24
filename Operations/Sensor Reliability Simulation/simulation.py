import numpy as np
import pandas as pd
import simulation_functions as simfunc
from matplotlib.patches import Ellipse, Polygon
import matplotlib.pyplot as plt
import scipy.interpolate as spinter
import scipy.stats as stats
from matplotlib import cm
import matplotlib.animation as animation
import seaborn as sns

df = pd.read_csv(r"./data/samples.csv")
df["MC"] = simfunc.MC(df["RH"].values, df["temp"].values)
df["FFDI"] = simfunc.FFDI(df["MC"].values, df["wind_spd"].values)
df["R"] = simfunc.R(df["FFDI"].values, 23.57)/3.6
df["LB"] = 1+10*(1-np.exp(-0.06*(1/3.6)*df["wind_spd"].values))
df = df[df.FFDI > 11]
df["wind_dir"] = 270-df["wind_dir"]
df = df[df.temp > 22]
df.index = np.arange(len(df))

t_max = 8*60
N, M = 100, len(df)
size = 10000
x_spacing, y_spacing = 280, 280
x_sensor = np.arange(0, size+x_spacing, x_spacing)
y_sensor = np.arange(0, size+y_spacing, y_spacing)
mesh_points = np.vstack(
    map(np.ravel, np.meshgrid(x_sensor, y_sensor))).transpose()
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


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def get_concentration(xy, centre, wind_dir, i, width_triangle, t):
    coord_diff = np.array([[xy[0] - centre[0]],
                           [xy[1] - centre[1]]])
    T = np.array([[np.cos(np.deg2rad(wind_dir)), -np.sin(np.deg2rad(wind_dir))],
                  [np.sin(np.deg2rad(wind_dir)), np.cos(np.deg2rad(wind_dir))]])
    coord = T@coord_diff + np.array([[width_triangle[-1]/2],
                                     [0]])
    x_arr = np.linspace(
        width_triangle[0], width_triangle[-1], len(t))
    data = simfunc.concentration_distribution(x_arr[1:])
    Z = np.array([C0_init_ppm[i+1]*simfunc.density_plot(x_arr[1:],
                                                        params[0], params[1]) for params in data])
    idx = np.array([np.round(coord[0][0]/width_triangle[-1] * len(t)),
                    np.round(coord[1][0]/width_triangle[-1] * len(t))], dtype=int)
    concentration = Z[idx[0]][idx[1]]
    return concentration


run = True
if run:
    for index, t in enumerate(time):
        if index < 1:
            print(f"Running try no. {index+1}")
            x_f, y_f = np.random.uniform(0, size, 2)
            R, lb, wind_dir, wind_spd, temp = df.iloc[index]["R"], df.iloc[index][
                "LB"], df.iloc[index]["wind_dir"], df.iloc[index]["wind_spd"], df.iloc[index]["temp"]
            length_ellipse, width_ellipse, centre = simfunc.ellips_params(
                t, R, lb)
            length_triangle, width_triangle = simfunc.cone_params(
                t, wind_spd/3.6, lb)
            centre = [x_f+centre*np.cos(np.deg2rad(wind_dir)),
                      y_f + centre*np.sin(np.deg2rad(wind_dir))]

            C0_init_ppm = initial_concentrations(t)[0]

            print(get_concentration(
                (centre[0][index]+100, centre[1][index]+100), (centre[0][index], centre[1][index]), wind_dir, 50, width_triangle, t))

            plotting = False
            if plotting:
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
                    X, T = np.meshgrid(x[begin_N:], t[begin_N:])
                    Z = np.array([C0_init_ppm[i+1]*simfunc.density_plot(x[begin_N:],
                                                                        params[0], params[1]) for params in data])
                    sns.heatmap(Z, vmin=0.0, vmax=0.050, cmap="Greys")

                anim = animation.FuncAnimation(
                    fig, animate, init_func=init, frames=20, repeat=False)

                plt.show()

    #     for i in range(N):
    #         print(f"Running time step no. {i+1}")
    #
    #         ellipse_patches = Ellipse((centre[0][i], centre[1][i]), length_ellipse[i], width_ellipse[i],
    #                                 wind_dir, facecolor="none", edgecolor="orange", linewidth="0.2")

    #         triangle_points = simfunc.triangle_points(
    #             length_triangle, width_triangle, centre, wind_dir, i)

    #         triangle_patches = Polygon(
    #             triangle_points, closed=True, facecolor="none", edgecolor="grey", linewidth="0.2")

        # detection_gas = simfunc.detection_time(triangle_patches, mesh_points,wind_dir,np.array([centre[0][i],centre[1][i]]), (c0_conc, h2_conc), width_triangle[i])
        # print(detection_gas)
        # print(detection_gas)
        # if detection_gas == True:
        #     detection_time_gas = time[0][i]
        #     df.loc[index, "detection_time_gas"] = detection_time_gas
        #     break

        # plotting = False
        # if plotting:
        #     fig, ax = plt.subplots(figsize=(8, 8))
        #     for i, ellipse in enumerate(ellipse_patches):
        #         ax.add_patch(ellipse)
        #         ax.add_patch(triangle_patches[i])
        #     ax.scatter(mesh_points[:, 0], mesh_points[:, 1])
        #     plt.scatter(x_f, y_f, color='red')
        #     plt.xlim(0, size)
        #     plt.ylim(0, size)
        #     plt.title(
        #         f'Wind Direction: {np.round(wind_dir, 0)} [deg], Wind Direction: {np.round(wind_spd, 2)} [km/h], Temperature: {np.round(temp, 2)} [C]')
        #     plt.show()

    # print(df)
    # df.to_csv(r"./data/fire_detection_time.csv")
