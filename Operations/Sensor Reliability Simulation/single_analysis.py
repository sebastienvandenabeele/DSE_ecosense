import pandas as pd
import numpy as np

if __name__ == "__main__":
    df = pd.read_csv(r"./data/fire_detection_time_.csv")

    df.loc[df['detection_time_gas'] <= 10*60, "detection_time_good"] = 1
    df.loc[df['detection_time_gas'] > 10*60, "detection_time_good"] = 0

    reliability = (df['detection_time_good']
                   [df['detection_time_good'] != 0].count())/df.shape[0]

    average_detection_time = df["detection_time_gas"].mean()

    print(df)

    print(
        f"\nReliability (within 10 minutes): {np.round(reliability*100, 2)}%")
    print(
        f"\nAverage detection time: {np.round(df['detection_time_gas'].mean()/60, 2)} [min]")
