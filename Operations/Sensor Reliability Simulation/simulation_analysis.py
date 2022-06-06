from turtle import color
import numpy as np
import pandas as pd
import gui_functions as gui
import mesh_types
import matplotlib.pyplot as plt
import itertools


def get_reliability(probability_range, likelihood):
    return probability_range[0] + likelihood*(probability_range[1]-probability_range[0])


if __name__ == "__main__":
    N = 51
    plotting_df = pd.DataFrame(columns=["reliability"], index=np.arange(N))
    for i in range(N):
        df = pd.read_csv(r"./data/fire_detection_time_"+str(i)+".csv")

        df.loc[df['detection_time_gas'] < 10*60, "detection_time_good"] = 1
        df.loc[df['detection_time_gas'] > 10*60, "detection_time_good"] = 0

        plotting_df.loc[i, "reliability"] = (df['detection_time_good']
                                             [df['detection_time_good'] != 0].count())/df.shape[0]

        plotting_df.loc[i,
                        "avg_detection_time"] = df["detection_time_gas"].mean()
        
        plotting_df.loc[i, "max_fire_size"] = df["fire_area"].max()

    
    spacing_range = np.linspace(300, 550, 51)
    shift_range = [0.]
    iteration_list = list(itertools.product(
        spacing_range, shift_range))

    plotting_df["spacing"] = [item[0] for item in iteration_list]
    plotting_df["shift"] = [item[1] for item in iteration_list]

    x_spacing_rel = [np.round(plotting_df[plotting_df["spacing"] == x]
                              ["reliability"].mean() * 100, 2) for x in spacing_range]
    shift_rel = [np.round(plotting_df[plotting_df["shift"] == shift]
                          ["reliability"].mean() * 100, 2) for shift in shift_range]

    spacing_array = np.flip([float(spacing)
                             for spacing in plotting_df["spacing"].values])
    reliability_array = np.flip([float(reliability)
                                 for reliability in plotting_df["reliability"].values*100])

    z = np.polyfit(reliability_array, spacing_array, 5)
    f = np.poly1d(z)

    x_new = np.linspace(
        np.min(reliability_array), np.max(reliability_array), len(reliability_array))
    y_new = f(x_new)

    ybar = np.sum(spacing_array)/len(spacing_array)
    ssreg = np.sum((y_new-ybar)**2)
    sstot = np.sum((spacing_array - ybar)**2)
    r_squared = ssreg / sstot

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(x_new, y_new, label="Curve Fit")
    ax.plot(reliability_array,
            spacing_array, label="Raw Data")
    ax.set_xlabel("Reliability [%]")
    ax.set_ylabel('Spacing [m]')
    ax.legend()
    ax.grid()
    ax.text(65.7, 472, "R²: "+str(np.round(r_squared, 4)))
    fig.savefig('./figures/curve_fit.png')
    plt.show()

    df = pd.read_csv("../Flight_software/data/prob_density.csv")
    likelihood = df["likelihood"].values
    probabilities = df["fire_prob"].values
    df["rel_req"] = get_reliability((55, 75), likelihood)
    df["spacing_req"] = f(df["rel_req"].values)
    df["nbr_sensor"] = np.floor(1500/df["spacing_req"].values)**2

    final_park_reliability = np.round(
        np.dot(df["rel_req"].values, probabilities), 2)
    park_nbr_sensors = int(df["nbr_sensor"].sum())
    constant_spacing_nbr_sensor = int(
        np.floor(1500/f(final_park_reliability))**2 * 3770)
    variable_vs_constant = constant_spacing_nbr_sensor - park_nbr_sensors
    minimum_spacing = np.round(np.min(df["spacing_req"].values), 2)
    maximum_spacing = np.round(np.max(df["spacing_req"].values), 2)
    # print(df)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.hist(df["spacing_req"].values)
    ax.set_xlabel("Sensor Spacing [m]")
    ax.set_ylabel("Subtile Count [-]")
    # fig.savefig('./figures/sensor_spacing_distribution.png')
    # plt.show()

    print(f"Minimum Spacing: {minimum_spacing} [m]")
    print(f"Maximum Spacing: {maximum_spacing} [m]")
    print(f"Reliability: {final_park_reliability}%")
    print(f"Variable mesh nbr. of sensors: {park_nbr_sensors}")
    print(f"Constant mesh nbr. of sensors: {constant_spacing_nbr_sensor}")
    print(f"Variable vs. Constant mesh: {variable_vs_constant}")

    def create_optimised_mesh(df):
        x_shift, y_shift = 0, 0
        lat, long = -33.673333, 150.146369
        mesh_fin = np.empty((len(df["spacing_req"]), 2))
        for idx in range(len(df["spacing_req"])):
            spacing_temp = df["spacing_req"][idx]
            mesh_temp = mesh_types.mesh1(1500, spacing_temp).tolist()
            mesh_temp_2 = [i for i in mesh_temp]
            for j in range(len(mesh_temp)):
                if mesh_temp[j][0] > 1500 or mesh_temp[j][1] > 1500:
                    mesh_temp_2.remove([mesh_temp[j][0], mesh_temp[j][1]])
            mesh_temp_array = np.array(mesh_temp_2)
            long_temp = df["lon"][idx]
            lat_temp = df["lat"][idx]
            if long_temp != long:
                y_shift += 1500
                x_shift = 0
            if lat_temp > lat:
                x_shift += 1500
            mesh_temp_array[:][0] += x_shift
            mesh_temp_array[:][1] += y_shift
            mesh_fin[i] = mesh_temp_array
        return mesh_fin


    # mesh = create_optimised_mesh(df)
    # print(mesh[0, 0])
    # gui.mesh_plot(mesh, 100000)

    plotting = False
    if plotting:
        df["detected"] = df["detected"].astype(int)
        mesh_points = mesh_types.mesh1(10000, 200, 200, 0)
        # gui.draw_overall_reliabilities(
        #     x_spacing_rel, y_spacing_rel, shift_rel, x_spacing_range, y_spacing_range, shift_range)
        # gui.detected_corr(df)
        # gui.detected_map(mesh_points, pd.read_csv(
        #     r"./data/fire_detection_time_0.csv"))
        # gui.draw_reliability(plotting_df)
