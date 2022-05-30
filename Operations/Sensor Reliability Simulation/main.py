import itertools
import simulation
import mesh_types
import numpy as np
import simulation_functions as simfunc

x_spacing_range = [200, 300, 400]
y_spacing_range = [200, 300, 400]
shift_range = [0., 0.25, 0.5, 0.75]

df = simfunc.read_and_edit_samples("./data/samples.csv")
t_max = 10*60
threshold = 0.05
N, M = int(100*(t_max/(8*60))), len(df)
size = 10000
gas = "CO"

if __name__ == "__main__":
    iteration_list = [list(itertools.product(
        x_spacing_range, y_spacing_range, shift_range))[0]]
    # for i, iteration in enumerate(iteration_list):
    iteration = [300, 300, 0]
    mesh_points = mesh_types.mesh1(
        size, iteration[0], iteration[1], iteration[2])
    time = np.linspace(0, t_max, N)*np.ones((M, 1))
    simulation.simulate(mesh_points, time, 0, df,
                        threshold, N, size, gas, t_max, plotting=True)
