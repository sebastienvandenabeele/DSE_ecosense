import numpy as np
import scipy.optimize as sco
import time

start_time = time.time()


def get_reliability(M):
    reliability = np.random.uniform(0.4, 0.85, M)
    return reliability


def get_concentrations(M):
    concentration = np.random.random(M)
    return concentration/np.sum(concentration)


N = 10000000
M = 100
result = 0
reliability = np.empty(M)
concentration_map = get_concentrations(M)

for i in range(N):
    reliability_temp = get_reliability(M)
    result_temp = np.dot(reliability_temp, concentration_map)
    if np.abs(0.62-result_temp) < np.abs(0.62-result):
        result = result_temp
        reliability = reliability_temp

print(result)
print(reliability)

print("--- %s seconds ---" % (time.time() - start_time))