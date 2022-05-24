import numpy as np
import pandas as pd
import simulation_functions as simfunc
from matplotlib.patches import Ellipse, Polygon
import matplotlib.pyplot as plt

df = pd.read_csv(r"./data/fire_detection_time.csv")
df["detection_time_gas"].plot.hist()
plt.xlabel("fire detection time")
plt.show()

