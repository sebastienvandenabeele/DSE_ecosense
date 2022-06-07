import numpy as np
import matplotlib.pyplot as plt

arr = np.array([[0.5, 59052],
                [1 ,14706],
                [1.5, 6536],
                [2.0, 3648],
                [4 ,896],
                [6 ,399],
                [8, 224],
                [10 ,132]])

arr2 = np.array([[0.5, 40728.],
               [1 ,10053],
                [1.5 ,4430],
                [2.0 ,2454],
                [4 ,579],
                [6 ,251],
                [8 ,135],
                [10 ,76]])

plt.plot(arr2[:,0],arr2[:,1],label="subtiles in the park")
plt.xlabel("subtile spacing [km]")
plt.ylabel("number of subtiles")
plt.legend()
plt.show()