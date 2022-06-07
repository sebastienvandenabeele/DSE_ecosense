import folium
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import atan2

mesh_df = pd.read_csv(r"./data/custom_mesh.csv").iloc[2:,:]
plt.scatter(mesh_df["lon"],mesh_df["lat"])
plt.show()
