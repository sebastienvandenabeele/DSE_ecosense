import simulation
import simulation_functions as simfunc
import numpy as np
import mesh_types

iteration = [400, 300, 0.75]

df = simfunc.read_and_edit_samples("./data/samples.csv")
t_max = 10*60
threshold = 0.05
N, M = int(100*(t_max/(8*60))), len(df)
size = 10000
gas = "CO"

if __name__ == "__main__":
    mesh_points = mesh_types.mesh1(
        size, iteration[0], iteration[1], iteration[2])
    time = np.linspace(0, t_max, N)*np.ones((M, 1))
    simulation.simulate(mesh_points, time, 0, df,
                        threshold, N, size, gas, t_max, 1000, plotting=False, saving=False)
