import numpy as np
import pandas as pd
import gui_functions as gui
import itertools


def get_reliability(probability_range, likelihood):
    return probability_range[0] + likelihood*(probability_range[1]-probability_range[0])


if __name__ == "__main__":
    N = 27
    plotting_df = pd.DataFrame(columns=["reliability"], index=np.arange(N))
    for i in range(N):
        df = pd.read_csv(r"./testing_data/fire_detection_time_"+str(i)+".csv")

        df.loc[df['detection_time_gas'] < 10*60, "detection_time_good"] = 1
        df.loc[df['detection_time_gas'] > 10*60, "detection_time_good"] = 0

        plotting_df.loc[i, "reliability"] = (df['detection_time_good']
                                             [df['detection_time_good'] != 0].count())/df.shape[0]

        plotting_df.loc[i,
                        "avg_detection_time"] = df["detection_time_gas"].mean()

    x_spacing_range = [300, 400, 500]
    y_spacing_range = [300, 400, 500]
    shift_range = [0., 0.25, 0.5]
    iteration_list = list(itertools.product(
        x_spacing_range, y_spacing_range, shift_range))

    plotting_df["x_spacing"] = [item[0] for item in iteration_list]
    plotting_df["y_spacing"] = [item[1] for item in iteration_list]
    plotting_df["shift"] = [item[2] for item in iteration_list]

    x_spacing_rel = [np.round(plotting_df[plotting_df["x_spacing"] == x]
                              ["reliability"].mean() * 100, 2) for x in x_spacing_range]
    y_spacing_rel = [np.round(plotting_df[plotting_df["y_spacing"] == x]
                              ["reliability"].mean() * 100, 2) for x in y_spacing_range]
    shift_rel = [np.round(plotting_df[plotting_df["shift"] == shift]
                          ["reliability"].mean() * 100, 2) for shift in shift_range]

    corr = np.corrcoef(np.sort(plotting_df[plotting_df["x_spacing"] == 500]["reliability"].values.astype(float)),
                       np.sort(plotting_df[plotting_df["y_spacing"] == 500]["reliability"].values.astype(float)))

    print(corr)

    plotting = False
    if plotting:
        gui.draw_overall_reliabilities(
            x_spacing_rel, y_spacing_rel, shift_rel, x_spacing_range, y_spacing_range, shift_range)
