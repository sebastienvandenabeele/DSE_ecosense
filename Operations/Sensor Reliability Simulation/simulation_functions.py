import numpy as np
import scipy.stats as stats


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
    if lb < 1:
        lb = 1.1
    l = R*t
    w = l/lb
    c = np.sqrt((l/2)**2 - (w/2)**2)
    return np.array([l, w, c])


def cone_params(t, u, lb):
    """_summary_

    Args:
        t (_type_): _description_
        u (_type_): _description_
        lb (_type_): _description_

    Returns:
        _type_: _description_
    """
    if lb < 1:
        lb = 1.1
    l = u*t
    w = l/lb
    return np.array([l, w])


def triangle_points(l, w, centre, wind_dir, i):
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
    x1 = np.array([centre[0][i], centre[1][i]])
    x2 = x1 + (T@(np.array([l[i], w[i]/2]).reshape((2, 1)))).flatten()
    x3 = x1 + (T@(np.array([l[i], -w[i]/2]).reshape((2, 1)))).flatten()
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


def get_concentration(xy, centre, wind_dir, i, width_triangle, time_arr, C0_init_ppm):
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
    T = np.array([[np.cos(np.deg2rad(wind_dir)), -np.sin(np.deg2rad(wind_dir))],
                  [np.sin(np.deg2rad(wind_dir)), np.cos(np.deg2rad(wind_dir))]])
    coord = T@coord_diff + np.array([[width_triangle[-1]/2],
                                     [0]])
    x_arr = np.linspace(
        width_triangle[0], width_triangle[-1], len(time_arr))
    data = concentration_distribution(x_arr[1:])
    Z = np.array([C0_init_ppm[i]*density_plot(x_arr[1:],
                                              params[0], params[1]) for params in data])
    idx = np.array([np.round(coord[0][0]/width_triangle[-1] * len(time_arr)),
                    np.round(coord[1][0]/width_triangle[-1] * len(time_arr))], dtype=int)
    try:
        concentration = Z[idx[0]][idx[1]]
    except:
        concentration = 0
    return concentration
