import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from scipy import stats

if __name__ == "__main__":
    data = pd.read_excel(r"./data/temperature_data.xlsx")
    wind_directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE",
                       "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW", "N"]
    wind_angles = [22.5*s for s in range(len(wind_directions))]
    wind_directions_card, wind_angles = wind_directions[1:], wind_angles[1:]
    wind_zip = zip(wind_directions_card, wind_angles)
    wind_dir = dict(wind_zip)
    data["wind_dir"] = np.array([wind_dir[direction]
                                for direction in data["wind_dir"].values])
    wind_directions = ["land wind", "sea wind"]
    data["wind_dir_dummy"] = np.array(
        [1 if 180 <= direction <= 360 else 0 for direction in data["wind_dir"].values])
    data["wind direction"] = ["land" if direction ==
                              1 else "sea" for direction in data["wind_dir_dummy"].values]

    def normal_distr_params(x):
        return np.mean(x), np.std(x)

    def normal_pdf(x):
        mu, sig = np.mean(x), np.std(x)
        s = np.arange(np.min(x), np.max(x), 0.01)
        return [s, stats.norm.pdf(s, mu, sig)]

    data_distribution = pd.DataFrame([])
    parameters = ["max_temp", "RH", "wind_spd"]
    samples = pd.DataFrame([])
    conf_level = 1.65
    N = 70000
    for parameter in parameters:
        mu, sig = normal_distr_params(data[parameter])
        data_distribution.loc["mu", parameter] = mu
        data_distribution.loc["sig", parameter] = sig
        s = np.random.normal(mu, sig, N)
        Z = (s-mu)/(sig)
        if parameter == "max_temp" or parameter == "wind_spd":
            s = s[Z > conf_level]

        else:
            s = s[Z < -conf_level]

        param_sample = pd.DataFrame({parameter: s})
        samples = pd.concat([samples, param_sample], axis=1, ignore_index=True)

    samples.columns = parameters
    samples = samples.dropna()
    samples["wind_dir"] = np.random.uniform(225, 315, len(samples))
    print(data_distribution)
    samples.to_csv("./data/samples.csv", index=False)

    def MC(RH, T):
        return 5.658+0.04651*RH+0.0003151*(RH**3)/T - 0.184*T**(0.77)

    def FFDI(mc, U):
        return 34.81*np.exp(0.987*np.log(10))*(mc**(-2.1))*np.exp(0.0234*U)

    def R(ffdi, w):
        return 0.0012*ffdi*w

    samples = samples[samples["RH"] > 10]
    samples.to_csv("./data/samples.csv", index=False)
    samples["MC"] = MC(samples["RH"].values, samples["max_temp"].values)
    samples["FFDI"] = FFDI(samples["MC"].values, samples["wind_spd"].values)
    samples["R"] = R(samples["FFDI"].values, 18)

    plot = True
    if plot:
        fig, ax = plt.subplots(2, 2)
        ax[0, 0].hist(samples["R"], color="tab:red")
        ax[0, 0].set_xlabel("R [km/h]")

        ax[0, 1].scatter(samples["max_temp"], samples["R"],
                         c=samples["MC"], cmap="Reds_r")
        ax[0, 1].set_xlabel("Temperature [C]")
        ax[0, 1].set_ylabel("Rate of spread [km/h]")

        ax[1, 0].scatter(samples["RH"], samples["R"],
                         c=samples["MC"], cmap="Reds_r")
        ax[1, 0].set_xlabel("Relative Humidity [%]")
        ax[1, 0].set_ylabel("Rate of spread [km/h]")

        c = ax[1, 1].scatter(samples["wind_spd"], samples["R"],
                             c=samples["MC"], cmap="Reds_r")
        ax[1, 1].set_xlabel("Wind speed [km/h]")
        ax[1, 1].set_ylabel("Rate of spread [km/h]")
        plt.subplots_adjust(wspace=0.25, hspace=0.5, right=0.8)
        cax = plt.axes([0.85, 0.1, 0.075, 0.8])
        cbar = plt.colorbar(c, cax=cax)
        cbar.ax.set_title('Moisture Content')

        fig, ax = plt.subplots(2, 3)
        ax[0, 0].hist(data["max_temp"], density=True)
        s, pdf = normal_pdf(data["max_temp"])
        ax[0, 0].plot(s, pdf, linewidth=2)
        ax[0, 0].set_xlabel("maximum temperature [deg C]")

        ax[1, 0].hist(data["RH"], density=True)
        s, pdf = normal_pdf(data[data["RH"] < 100]["RH"])
        ax[1, 0].plot(s, pdf, linewidth=2)
        ax[1, 0].set_xlabel("relative humidity [%]")

        ax[1, 1].hist(data["wind_spd"], density=True)
        s, pdf = normal_pdf(data["wind_spd"])
        ax[1, 1].plot(s, pdf, linewidth=2)
        ax[1, 1].set_xlabel("wind speed [km/h]")

        ax[0, 2].hist(data["wind direction"], density=True)
        ax[0, 2].set_xlabel("binary wind direction")

        bins = np.linspace(0, 2*np.pi, 18)
        n, bins = np.histogram(np.deg2rad(
            data["wind_dir"]), bins=bins, density=True)
        ax[0, 1].axis("off")
        polar_ax = fig.add_subplot(232, polar=True)
        bars = polar_ax.bar(np.flip(bins[1:])+np.pi/2, n)
        polar_ax.set_xticks([0, np.pi/2, np.pi, 1.5*np.pi, 2*np.pi])
        polar_ax.set_yticklabels([])
        polar_ax.set_xticklabels(['E', 'N', 'W', 'S', ''])
        polar_ax.set_xlabel("cardinal wind direction")

        corr_matrix = data[["max_temp", "RH",
                            "wind_spd", "wind_dir_dummy"]].corr()
        headers = ["temp", "hum", "wind spd", "wind dir"]
        corr_matrix.columns = headers
        corr_matrix.index = headers
        corr_heatmap = seaborn.heatmap(corr_matrix,
                                       xticklabels=corr_matrix.columns,
                                       yticklabels=corr_matrix.columns, ax=ax[1, 2], cmap="RdYlGn", vmin=-1, vmax=1)
        corr_heatmap.set_xticklabels(
            corr_heatmap.get_xticklabels(), rotation=0, horizontalalignment='center')
        corr_heatmap.set_yticklabels(
            corr_heatmap.get_yticklabels(), rotation=0, horizontalalignment='right')
        ax[1, 2].set_xlabel("correlation matrix")
        plt.title("Nullo Mountain Weather Data", fontsize=18)
        plt.subplots_adjust(wspace=0.25, hspace=0.5)

        fig, ax = plt.subplots(2, 2)
        ax[0, 0].hist(samples["max_temp"], density=True)
        ax[0, 0].set_xlabel("maximum temperature [deg C]")

        ax[1, 0].hist(samples["RH"], density=True)
        ax[1, 0].set_xlabel("relative humidity [%]")

        ax[1, 1].hist(samples["wind_spd"], density=True)
        ax[1, 1].set_xlabel("wind speed [km/h]")

        bins = np.linspace(0, 2*np.pi, 18)
        n, bins = np.histogram(np.deg2rad(
            samples["wind_dir"]), bins=bins, density=True)
        ax[0, 1].axis("off")
        polar_ax = fig.add_subplot(222, polar=True)
        bars = polar_ax.bar(np.flip(bins[1:])+np.pi/2, n)
        polar_ax.set_xticks([0, np.pi/2, np.pi, 1.5*np.pi, 2*np.pi])
        polar_ax.set_yticklabels([])
        polar_ax.set_xticklabels(['E', 'N', 'W', 'S', ''])
        polar_ax.set_xlabel("cardinal wind direction")
        fig.suptitle("High Wildfire Risk Weather Samples", fontsize=18)
        plt.subplots_adjust(wspace=0.25, hspace=0.5)

        plt.show()
