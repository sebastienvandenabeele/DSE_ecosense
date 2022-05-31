from turtle import color
import numpy as np
import pandas as pd
import gui_functions as gui
import mesh_types
import matplotlib.pyplot as plt
import itertools

if __name__ == "__main__":
    plotting_df = pd.DataFrame(columns=["reliability"], index=np.arange(36))
    for i in range(36):
        df = pd.read_csv(r"./data/fire_detection_time_"+str(i)+".csv")

        df.loc[df['detection_time_gas'] < 8*60, "detection_time_good"] = 1
        df.loc[df['detection_time_gas'] > 8*60, "detection_time_good"] = 0

        plotting_df.loc[i, "reliability"] = (df['detection_time_good']
                                             [df['detection_time_good'] != 0].count())/df.shape[0]

        plotting_df.loc[i,
                        "avg_detection_time"] = df["detection_time_gas"].mean()

    x_spacing_range = [200, 300, 400]
    y_spacing_range = [200, 300, 400]
    shift_range = [0., 0.25, 0.5, 0.75]
    iteration_list = list(itertools.product(
        x_spacing_range, y_spacing_range, shift_range))

    plotting_df["x_spacing"] = [item[0] for item in iteration_list]
    plotting_df["y_spacing"] = [item[1] for item in iteration_list]
    plotting_df["shift"] = [item[2] for item in iteration_list]

    x_spacing_rel = [np.round(plotting_df[plotting_df["x_spacing"] == x]
                              ["reliability"].mean() * 100 * 14.2, 2) for x in x_spacing_range]
    y_spacing_rel = [np.round(plotting_df[plotting_df["y_spacing"] == y]
                              ["reliability"].mean() * 100 * 14.2, 2) for y in y_spacing_range]
    shift_rel = [np.round(plotting_df[plotting_df["shift"] == shift]
                          ["reliability"].mean() * 100 * 14.2, 2) for shift in shift_range]

    print(plotting_df)
    plotting = False
    if plotting:
        df["detected"] = df["detected"].astype(int)
        mesh_points = mesh_types.mesh1(10000, 200, 200, 0)
        gui.draw_overall_reliabilities(
            x_spacing_rel, y_spacing_rel, shift_rel, x_spacing_range, y_spacing_range, shift_range)
        # gui.detected_corr(df)
        # gui.detected_map(mesh_points, pd.read_csv(
        #     r"./data/fire_detection_time_0.csv"))
        # gui.draw_reliability(plotting_df)
