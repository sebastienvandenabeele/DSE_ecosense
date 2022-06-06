import numpy as np
import scipy.stats as stats
import pandas as pd
import scipy.interpolate as spinter


def read_and_edit_samples(filepath):
    """Reads the samples and creates a corresponding df. Also adds some necessary values for the simulation.

    Args:
        filepath (str): path of the samples CSV file

    Returns:g all the information necessary to the simulation
    """
    df = pd.read_csv(filepath)
    df["wind_spd"] = df["wind_spd"]*0.5
    df["MC"] = MC(df["RH"].values, df["temp"].values)
    df["FFDI"] = FFDI(df["MC"].values, df["wind_spd"].values)
    df["R"] = R(df["FFDI"].values, 23.57)/3.6
    df["LB"] = 1+10*(1-np.exp(-0.06*(1/3.6)*df["wind_spd"].values))
    df = df[df.FFDI > 11]
    df["wind_dir"] = 270-df["wind_dir"]
    df = df[df.temp > 22]
    df.index = np.arange(len(df))
    return df


def initial_gas_concentration(gas_type, t):
    """Gets the gas concentration emitted from a fire t seconds after ignition

    Args:
        gas_type (str): currently supports "CO" and "H2"
        t (float): time after wildfire starts [s]

    Returns:
        float: concentration pf the gas emitted from the wildfire at that time [ppm]
    """
    concentration_arr = pd.read_csv(
        "./data/gas_concentrations.csv", usecols=[gas_type]).to_numpy().flatten()
    time_concentrations = np.arange(0, 14, 1)

    concentration_function = spinter.interp1d(
        time_concentrations, concentration_arr)

    return concentration_function(t/60)


def get_relevant_detection_nodes(centre, mesh_points, wind_dir, length_triangle):
    """Gets the nodes within a circle (given a radius) centred at the fire ellipse center

    Args:
        centre (ndarray): array containing all the centre points of the fires throughout time
        radius (float): radius around the fire centre [m]
        mesh_points (ndarray): array containing all the sensor nodes [m, m]
        i (int): time index [-]

    Returns:
        ndarray: mesh array containing the relevant poins [m, m]
    """
    x0, y0, radius = (centre[0]+length_triangle/2 * np.cos(np.deg2rad(wind_dir))
                      ), (centre[1]+length_triangle/2 * np.sin(np.deg2rad(wind_dir))), length_triangle/2
    relevant_arg = np.argwhere(
        np.sqrt((mesh_points[:, 0]-x0)**2 + (mesh_points[:, 1]-y0)**2) < radius)
    return mesh_points[relevant_arg][:, 0, :]


def MC(rh, t):
    """Calculates moisture contents of a eucalypt forest wildfire

    Args:
        RH (float): Relative Humidity in % (eg. 65)
        T (float): Temperature in Degrees Celsius (eg. 30)

    Returns:
        float: Moisture Content
    """
    return 5.658+0.04651*rh+(0.0003151*(rh**3)/t)-0.184*(t**0.77)


def FFDI(mc, u):
    """Calculates the Forest Fire Danger Index

    Args:
        MC (float): Moisture contents
        U (float): Wind Speed in km/h

    Returns:
        float: FFDI
    """
    return (34.81*np.exp(0.987*np.log(10))*(mc)**(-2.1))*(np.exp(0.0234*u))


def R(ffdi, w):
    """Calculates the fire rate of spread in the direction of the wind

    Args:
        ffdi (float): Forest fire danger index
        w (float): Fuel load in t/ha (23.57)

    Returns:
        float: fire rate of spread in the direction of the wind
    """
    return 0.0012*ffdi*w


def ellips_params(t, R, lb):
    """Determines main parameters of an ellipse (major/minor axis and focal point position)

    Args:
        t (float): time [s]
        R (float): fire rate of spread [m/s]
        lb (float): length to width ratio of ellipse [-]

    Returns:
        ndarray: length, width and focal point position [m]
    """
    if isinstance(lb, np.ndarray):
        if np.shape(lb)[0] > 1:
            for i in range(len(lb)):
                if lb[i] < 1:
                    lb[i] = 1.1
    l = R*t
    w = l/lb
    c = np.sqrt((l/2)**2 - (w/2)**2)
    return l, w, c


def cone_params(t, u, lb):
    """Gets the cone paramaters corresponding to the smoke emitted from a wildfire

    Args:
        t (float): time from cone start [s]
        u (float): wind speed [m/s]
        lb (float): cone slenderness ratio [-]

    Returns:
        ndarray: array containing the lengths and widths of the triangle at the given time (from start of the cone, thus t=0 should yield l=w=0)
    """
    l = u*t
    w = l/lb
    return np.array([l, w])


def triangle_points(l, w, centre, wind_dir):
    """Gets the point location of the cone based on length, width and wind direction

    Args:
        l (float): length [m]
        w (float): width [m]
        centre (tuple): contains x and y position of the ellipse centre [m]
        wind_dir (float): wind angle from horizontal (ccw) [deg]
        i (int): iteration

    Returns:
        1darray: contains the three points rotated according to the wind [m]
    """
    T = np.array([[np.cos(np.deg2rad(wind_dir)), -np.sin(np.deg2rad(wind_dir))],
                  [np.sin(np.deg2rad(wind_dir)), np.cos(np.deg2rad(wind_dir))]])
    x1 = np.array([centre[0], centre[1]])
    x2 = x1 + (T@(np.array([l, w/2]).reshape((2, 1)))).flatten()
    x3 = x1 + (T@(np.array([l, -w/2]).reshape((2, 1)))).flatten()
    return np.array([x1, x2, x3])


def concentration_distribution(x):
    """Determines the normal distribution based where 95.5% of values are located between the first and last x array value

    Args:
        x (1darray): x (width) array

    Returns:
        1darray: array containing the average and standard deviation of the computed normal distribution
    """
    mu = (x[-1]-x[0])/2
    sigs = x/4
    return np.array([[mu, sig] for sig in sigs])


def density_plot(x, mu, sig):
    """Plots the normal desnity function based on x and its parameters

    Args:
        x (1darray): x (width) array
        mu (float): average
        sig (float): standard deviation

    Returns:
        1darray: array containing the normal distribution
    """
    return stats.norm.pdf(x, loc=mu, scale=sig)


def get_concentration(xy, centre, wind_dir, i, width_triangle, length_triangle, time_arr, C0_init_ppm):
    """_summary_

    Args:
        xy (_type_): _description_
        centre (_type_): _description_
        wind_dir (_type_): _description_
        i (_type_): _description_
        width_triangle (_type_): _description_
        time_arr (_type_): _description_
        C0_init_ppm (_type_): _description_

    Returns:
        _type_: _description_
    """
    coord_diff = np.array([[xy[0] - centre[0]],
                           [xy[1] - centre[1]]])
    T = np.array([[np.cos(np.deg2rad(-wind_dir)), -np.sin(np.deg2rad(-wind_dir))],
                  [np.sin(np.deg2rad(-wind_dir)), np.cos(np.deg2rad(-wind_dir))]])
    coord = np.flip(T@coord_diff, axis=None) + \
        np.array([[width_triangle[-1]/2], [0]])
    x_arr = np.linspace(
        width_triangle[0], width_triangle[-1], len(time_arr))
    data = concentration_distribution(x_arr[1:])
    Z = np.array([C0_init_ppm[i]*density_plot(x_arr[1:],
                                              params[0], params[1]) for params in data])
    idx = np.array([np.round(coord[0][0]/width_triangle[-1] * len(time_arr)),
                    np.round(coord[1][0]/length_triangle[-1] * len(time_arr))], dtype=int)
    if idx[0] >= 0 and idx[1] >= 0:
        try:
            concentration = Z[idx[0]][idx[1]]
        except:
            concentration = 0
    else:
        concentration = 0
    return concentration


if __name__ == "__main__":
    print(initial_gas_concentration("H2", 60))
