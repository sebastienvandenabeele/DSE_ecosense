import numpy as np
import pandas as pd
import gui_functions as gui
import mesh_types

if __name__ == "__main__":
    df = pd.read_csv(r"./data/fire_detection_time.csv")

    mesh_points = mesh_types.mesh1(
        10000, 280, 280, 0)

    df.loc[df['detection_time_gas'] < 8*60, "detection_time_good"] = 1
    df.loc[df['detection_time_gas'] > 8*60, "detection_time_good"] = 0

    reliability = (df['detection_time_good']
                   [df['detection_time_good'] != 0].count())/df.shape[0]

    print(
        f"\nReliability (within 8 minutes): {np.round(reliability*100, 2)}%")
    print(
        f"\nAverage detection time: {np.round(df['detection_time_gas'].mean()/60, 2)} [min]")
    print(
        f"\nDetection time standard deviation: {np.round(df['detection_time_gas'].std()/60, 2)} [min]\n")

    plotting = True
    df["detected"] = df["detected"].astype(int)

    if plotting:
        # gui.detected_corr(df)
        gui.detected_map(mesh_points, df)
