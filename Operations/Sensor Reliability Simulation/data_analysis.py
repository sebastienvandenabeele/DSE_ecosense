import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn


if __name__ == "__main__":
    data = pd.read_excel(r"./data/temperature_data.xlsx")
    wind_directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE",
                       "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW", "N"]
    wind_angles = [22.5*s for s in range(len(wind_directions))]
    wind_directions, wind_angles = wind_directions[1:], wind_angles[1:]
    wind_zip = zip(wind_directions, wind_angles)
    wind_dir = dict(wind_zip)
    data["wind_dir"] = np.array([wind_dir[direction]
                                for direction in data["wind_dir"].values])
    wind_directions = ["land wind", "sea wind"]
    data["wind_dir_dummy"] = np.array(
        [0 if 180 <= direction <= 360 else 1 for direction in data["wind_dir"].values])
    data["wind direction"] = ["land" if direction ==
                              0 else "sea" for direction in data["wind_dir_dummy"].values]

    sel_months = ["oct", "dec", "jan", "feb", "march"]
    data = data[data.month.isin(sel_months)]

    def normal_distr_params(x):
        return np.mean(x), np.std(x)

    data_distribution = pd.DataFrame([])
    samples = pd.DataFrame([])
    N = 20000
    parameters = ["RH", "wind_dir", "wind_spd"]
    for parameter in parameters:
        mu, sig = normal_distr_params(data[parameter].values)
        data_distribution.loc["mu", parameter] = mu
        data_distribution.loc["sig", parameter] = sig

    data_distribution["temp"] = [24.3, 4.59144]

    for parameter in data_distribution.columns.values:
        mu, sig = data_distribution[parameter]
        s = np.random.normal(mu, sig, N)
        samples[parameter] = s

    samples = samples[samples.RH < 50]
    samples = samples[samples['wind_dir'].between(190, 350)]
    print(samples)

    samples.to_csv("./data/samples.csv", index=False)

    plot = False
    if plot:
        fig, ax = plt.subplots(3, 1, figsize=(10, 10))
        seaborn.scatterplot(ax=ax[0], data=data,
                            x="max_temp", y="RH", hue="wind direction")
        seaborn.scatterplot(ax=ax[1], data=data,
                            x="max_temp", y="RH", hue="month")
        seaborn.scatterplot(ax=ax[2], data=data,
                            x="max_temp", y="RH", hue="wind_spd")
        plt.show()
