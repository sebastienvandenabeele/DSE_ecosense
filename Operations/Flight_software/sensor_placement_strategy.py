import pandas as pd
import numpy as np

def sensor_placement_grid(p):

    df = pd.read_csv(r"./data/prob_density.csv")

    print(df)

sensor_placement_grid(1)