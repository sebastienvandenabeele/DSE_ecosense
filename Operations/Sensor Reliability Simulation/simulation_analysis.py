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

    spacing_range = np.linspace(300, 700, 51)
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
                             for spacing in plotting_df["spacing"].values][:34])
    reliability_array = np.flip([float(reliability)
                                 for reliability in plotting_df["reliability"].values*100][:34])

    z = np.polyfit(reliability_array, spacing_array, 5)
    f = np.poly1d(z)

    x_new = np.linspace(
        np.min(reliability_array), np.max(reliability_array), len(reliability_array)-1)
    y_new = f(x_new)

    ybar = np.sum(spacing_array)/len(spacing_array)
    ssreg = np.sum((y_new-ybar)**2)
    sstot = np.sum((spacing_array - ybar)**2)
    r_squared = ssreg / sstot

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(x_new, y_new, label="Curve Fit")
    ax.plot(reliability_array,
            spacing_array, label="Raw Data")
    ax.set_xlabel("Reliability [%]")
    ax.set_ylabel('Spacing [m]')
    ax.legend()
    ax.grid()
    ax.text(65.7, 472, "R²: "+str(np.round(r_squared, 4)))
    # fig.savefig('./figures/curve_fit.png')
    # plt.show()

    df = pd.read_csv("../Flight_software/data/prob_density.csv")
    likelihood = df["likelihood"].values
    probabilities = df["fire_prob"].values
    df["rel_req"] = get_reliability((55, 75), likelihood)
    df["spacing_req"] = f(df["rel_req"].values)
    df["nbr_sensor"] = np.floor(1500/df["spacing_req"].values)**2

    print(np.dot(df["rel_req"].values, probabilities))
    print(df)
    print(int(df["nbr_sensor"].sum()))

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
