import numpy as np
import pandas as pd
import simulation_functions as simfunc
from matplotlib.patches import Ellipse, Polygon
import matplotlib.pyplot as plt
import scipy.interpolate as spinter

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
N, M = 10, len(df)
size = 10000
x_spacing, y_spacing = 280, 280
x_sensor = np.arange(0, size+x_spacing, x_spacing)
y_sensor = np.arange(0, size+y_spacing, y_spacing)
mesh_points = np.vstack(
    map(np.ravel, np.meshgrid(x_sensor, y_sensor))).transpose()
time = np.linspace(0, t_max, N)*np.ones((M, 1))

C0_concentrations = np.array([0, 0.85, 4.55, 6.75, 10.6, 14.25, 17.9, 23.3, 28.5, 31.2, 34.55, 39.1, 42.7, 48.2])
H2_concentrations = 0.1*np.array([0,3,4,5,5,4,4,5,5,7,15,30,40,45])
time_concentrations = np.arange(0, 14, 1)

C0_concentration_function = spinter.interp1d(time_concentrations, C0_concentrations)
H2_concentration_function = spinter.interp1d(time_concentrations, H2_concentrations)

def initial_concentrations(t):
    return C0_concentration_function(t/60) , H2_concentration_function(t/60)

def concentration_distribution(w , c0):
    mu,sig = w/2 , (w/2)/(2)
    x = np.linspace(-w/2,w/2,1000)
    prob_density = c0*(np.pi*sig) * np.exp(-0.5*((x-mu)/sig)**2)
    return prob_density

run = True
if run:
    fig,ax = plt.subplots(N,1)
    for index, t in enumerate(time):
        print(f"Running try no. {index+1}")
        x_f, y_f = np.random.uniform(0, size, 2)
        R, lb, wind_dir, wind_spd, temp = df.iloc[index]["R"], df.iloc[index][
            "LB"], df.iloc[index]["wind_dir"], df.iloc[index]["wind_spd"], df.iloc[index]["temp"]
        length_ellipse, width_ellipse, centre = simfunc.ellips_params(t, R, lb)
        length_triangle, width_triangle = simfunc.cone_params(
            t, wind_spd/3.6, lb)
        centre = [x_f+centre*np.cos(np.deg2rad(wind_dir)),
                y_f + centre*np.sin(np.deg2rad(wind_dir))]
        
        C0_init_ppm = initial_concentrations(t)[0]
        print(C0_init_ppm)
        
      #  concentration_function = np.empty((N,1000))
      #  for i in range(N):
      #      concentration_function[i,:] = concentration_distribution(width_triangle[i] , C0_init_ppm)
            
      #  print(concentration_function[2])


    #     for i in range(N):
    #         print(f"Running time step no. {i+1}")
    #         
    #         ellipse_patches = Ellipse((centre[0][i], centre[1][i]), length_ellipse[i], width_ellipse[i],
    #                                 wind_dir, facecolor="none", edgecolor="orange", linewidth="0.2")

    #         triangle_points = simfunc.triangle_points(
    #             length_triangle, width_triangle, centre, wind_dir, i)

    #         triangle_patches = Polygon(
    #             triangle_points, closed=True, facecolor="none", edgecolor="grey", linewidth="0.2")

            #detection_gas = simfunc.detection_time(triangle_patches, mesh_points,wind_dir,np.array([centre[0][i],centre[1][i]]), (c0_conc, h2_conc), width_triangle[i])
            #print(detection_gas)
            #print(detection_gas)
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

    #print(df)
    #df.to_csv(r"./data/fire_detection_time.csv")
