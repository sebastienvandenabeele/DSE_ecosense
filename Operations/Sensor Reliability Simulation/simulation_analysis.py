from turtle import color
import numpy as np
import pandas as pd
import gui_functions as gui
import mesh_types
import matplotlib.pyplot as plt
import itertools

if __name__ == "__main__":
    N = 41
    plotting_df = pd.DataFrame(columns=["reliability"], index=np.arange(N))
    for i in range(N):
        df = pd.read_csv(r"./data/fire_detection_time_"+str(i)+".csv")

        df.loc[df['detection_time_gas'] < 10*60, "detection_time_good"] = 1
        df.loc[df['detection_time_gas'] > 10*60, "detection_time_good"] = 0

        plotting_df.loc[i, "reliability"] = (df['detection_time_good']
                                             [df['detection_time_good'] != 0].count())/df.shape[0]

        plotting_df.loc[i,
                        "avg_detection_time"] = df["detection_time_gas"].mean()

    spacing_range = np.linspace(300, 600, 41)
    shift_range = [0.]
    iteration_list = list(itertools.product(
        spacing_range, shift_range))

    plotting_df["spacing"] = [item[0] for item in iteration_list]
    plotting_df["shift"] = [item[1] for item in iteration_list]

    x_spacing_rel = [np.round(plotting_df[plotting_df["spacing"] == x]
                              ["reliability"].mean() * 100, 2) for x in spacing_range]
    shift_rel = [np.round(plotting_df[plotting_df["shift"] == shift]
                          ["reliability"].mean() * 100, 2) for shift in shift_range]

    plt.plot(plotting_df["spacing"], plotting_df["reliability"]*100)
    plt.show()
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
