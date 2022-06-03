import simulation
import simulation_functions as simfunc
import numpy as np
import mesh_types

iteration = [300, 0.5]

df = simfunc.read_and_edit_samples("./data/samples.csv")
t_max = 10*60
threshold = 0.05
N, M = int(100*(t_max/(8*60))), len(df)
size = 2000
gas = "CO"

if __name__ == "__main__":
    mesh_points = mesh_types.mesh1(
        size, iteration[0], iteration[1])
    time = np.linspace(0, t_max, N)*np.ones((M, 1))
    df = simulation.simulate(mesh_points, time, df,
                             threshold, N, size, gas, t_max, 1, plotting=False)
    print("Saving to CSV...")
    df.to_csv(r"./data/fire_detection_time_.csv")
