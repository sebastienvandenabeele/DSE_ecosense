import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == "__main__":
    df = pd.read_csv(r"./data/fire_detection_time.csv")
    reliability = (df['detection_time_gas']
                [df['detection_time_gas'] != 0].count())/df.shape[0]

    print(
        f"\nReliability (within 8 minutes): {np.round(reliability*100, 2)}%")
    print(
        f"\nAverage detection time: {np.round(df['detection_time_gas'].mean()/60, 2)} [min]")
    print(
        f"\nDetection time standard deviation: {np.round(df['detection_time_gas'].std()/60, 2)} [min]\n")

    plotting = False
    if plotting:
        df["detection_time_gas"].plot.hist()
        plt.xlabel("fire detection time")
        plt.show()
