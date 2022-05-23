import numpy as np


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
    l = u*t
    w = l/lb
    return np.array([l, w])


def triangle_points(l, w, centre, wind_dir, i):
    """_summary_

    Args:
        l (_type_): _description_
        w (_type_): _description_
        centre (_type_): _description_
        wind_dir (_type_): _description_
        i (_type_): _description_

    Returns:
        _type_: _description_
    """
    T = np.array([[np.cos(np.deg2rad(wind_dir)), -np.sin(np.deg2rad(wind_dir))],
                  [np.sin(np.deg2rad(wind_dir)), np.cos(np.deg2rad(wind_dir))]])
    x1 = np.array([centre[0][i], centre[1][i]])
    x2 = x1 + (T@(np.array([l[i], w[i]/2]).reshape((2, 1)))).flatten()
    x3 = x1 + (T@(np.array([l[i], -w[i]/2]).reshape((2, 1)))).flatten()
    return np.array([x1, x2, x3])