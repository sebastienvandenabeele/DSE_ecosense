import numpy as np
import pandas as pd
import simulation_functions as simfunc
import mesh_types
import gui_functions as plotting

df = simfunc.read_and_edit_samples("./data/samples.csv")

t_max = 8*60
threshold = 0.05
N, M = 100, len(df)
size = 10000
mesh_points = mesh_types.mesh1(size, 250, 350)
time = np.linspace(0, t_max, N)*np.ones((M, 1))


if __name__ == "__main__":
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
            C0_init_ppm = simfunc.initial_gas_concentration("CO", t)

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

    print("Saving to CSV...")
    df.to_csv(r"./data/fire_detection_time.csv")
