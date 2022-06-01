import itertools
import simulation
import mesh_types
import numpy as np
import simulation_functions as simfunc
from joblib import Parallel, delayed

spacing_range = np.linspace(300, 700, 51)
shift_range = [0.]

df = simfunc.read_and_edit_samples("./data/samples.csv")
t_max = 10*60
threshold = 0.05
N, M = int(100*(t_max/(8*60))), len(df)
size = 10000
gas = "CO"
iteration_list = list(itertools.product(spacing_range, shift_range))

def run(iteration_list):
    global df, t_max, threshold, N, M, size, gas
    for i, iteration in enumerate(iteration_list):
        mesh_points = mesh_types.mesh1(
            size, iteration[0], iteration[1])
        time = np.linspace(0, t_max, N)*np.ones((M, 1))
        df = simulation.simulate(mesh_points, time, df,
                            threshold, N, size, gas, t_max, 1000, plotting=False)
        print("Saving to CSV...")
        df.to_csv(r"./data/fire_detection_time_"+str(i)+".csv")
    

def multiprocessing_single_run(i):
    global iteration_list, df, t_max, threshold, N, M, size, gas
    mesh_points = mesh_types.mesh1(size, iteration_list[i][0], iteration_list[i][1])
    time = np.linspace(0, t_max, N)*np.ones((M, 1))
    df = simulation.simulate(mesh_points, time, df,
                        threshold, N, size, gas, t_max, 1000, plotting=False)
    print("Saving to CSV...")
    df.to_csv(r"./data/fire_detection_time_"+str(i)+".csv")


if __name__ == "__main__":
    Parallel(n_jobs=4, backend='multiprocessing', verbose=1)(delayed(multiprocessing_single_run)(i) for i in range(len(spacing_range)))
        
