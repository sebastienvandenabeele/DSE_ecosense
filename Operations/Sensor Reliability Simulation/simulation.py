import numpy as np
import pandas as pd
import simulation_functions as simfunc
import time as time_lib
import gui_functions as gui


def simulate(mesh_points, time, run_nbr, df, threshold, N, size, gas, t_max, chsn_idx, plotting=False, saving=False):
    start_time = time_lib.time()
    for index, t in enumerate(time):
        if index < chsn_idx:
            # print(f"Running try no. {index+1}...")

            # Get random fire location within mesh
            x_f, y_f = np.random.uniform(0, size, 2)
            df.loc[index, ["x_start", "y_start"]] = [x_f, y_f]

            # Determine parameters corresponding to the iteration sample
            R, lb, wind_dir, wind_spd, temp = df.iloc[index]["R"], df.iloc[index]["LB"], df.iloc[
                index]["wind_dir"], df.iloc[index]["wind_spd"], df.iloc[index]["temp"]

            # Get fire ellipse and cone parameters for the current iteration for all time steps
            length_ellipse, width_ellipse, centre_ellipse = simfunc.ellips_params(
                t, R, lb)
            length_triangle, width_triangle = simfunc.cone_params(
                t, wind_spd/3.6, lb)

            # Get the fire ellipse centre location for every time step in the current iteration
            centre = [x_f+centre_ellipse*np.cos(np.deg2rad(wind_dir)),
                      y_f+centre_ellipse*np.sin(np.deg2rad(wind_dir))]

            # Get the concentration of the gas emitted as the fire ellipse centre at every time step
            gas_init_ppm = simfunc.initial_gas_concentration(gas, t)

            upper_break = False

            # Get the relevant points given the fire ellipse centre (those that can realistically detect a fire)
            relevant_points = simfunc.get_relevant_detection_nodes(
                (x_f, y_f), mesh_points, wind_dir, length_triangle[-1])

            # Start the loop to go through time in the current iteration
            for time_idx in range(N):

                # Move on to next iteration as soon as the fire has been detected
                if upper_break:
                    break

                # Determine detection times of the fire at the current iteration by determining the concentration of every relevant node
                detection_times = []
                detection_point = []
                for i, xy in enumerate(relevant_points):
                    # Get sensor gas concentration
                    sensor_concentration_temp = simfunc.get_concentration(
                        (xy[0], xy[1]), (centre[0][i], centre[1][i]), wind_dir, time_idx, width_triangle, length_triangle, t, gas_init_ppm)

                    # Determine the extra time due to sensor placement wrt. to gas cone initial point
                    sensor_additional_time = time_idx/N * t_max

                    # Check if any sensor has detected a fire within the required time
                    if sensor_concentration_temp > threshold:

                        # Implement sensor manufacturer reliability and append detection time of the node that detected the fire
                        if np.random.uniform(0, 1) <= 0.92:
                            detection_times.append(
                                sensor_additional_time+t[time_idx])
                            detection_point.append(xy)

                detection_point_arr = np.array(detection_point)

                # Get the final detection time of the fire for the current iteration and break the loop
                if len(detection_times) != 0:
                    detection_time = np.floor(np.min(detection_times)/10)*10
                    print(f"Fire Detected!!! in {detection_time} [s]")
                    df.loc[index, "detection_time_gas"] = detection_time
                    df.loc[index, "detected"] = True
                    df.loc[index, "fire_area"] = np.pi * \
                        length_ellipse[time_idx]/2 * width_ellipse[time_idx]/2
                    upper_break = True

                else:
                    df.loc[index, "detected"] = False

            if plotting:
                gui.draw_patches(x_f, y_f, centre, length_ellipse, width_ellipse,
                                 wind_dir, length_triangle, width_triangle, wind_spd/3.6, temp, N, mesh_points, size, detection_point_arr, relevant_points)
            if saving:
                # Save data to a new CSV file
                print("Saving to CSV...")
                df.to_csv(r"./data/fire_detection_time_" + str(run_nbr) + ".csv")
            else:
                # Save data to a new CSV file
                print("Saving to CSV...")
                df.to_csv(r"./data/fire_detection_time_.csv")
    print("--- %s seconds ---" % (time_lib.time() - start_time))
