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
    l = R*t
    w = l/lb
    c = np.sqrt((l/2)**2 - (w/2)**2)
    return np.array([l, w, c])


def cone_params(t, u, lb):
    """Defines cone length and width

    Args:
        t (float): time [s]
        u (float): wind speed [m/s]
        lb (float): Cone slenderness ratio [-]

    Returns:
        1darray: Array containing length and width of the cone [m]
    """
    l = u*t
    w = l/(lb)
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


def detection_time(patch, points, wind_dir, centre, concentrations, width_triangle):
    """_summary_

    Args:
        patch (_type_): _description_
        points (_type_): _description_

    Returns:
        _type_: _description_
    """
    arg = np.argwhere(np.array([patch.contains_point(point)
                      for point in points]) == True)
    if len(arg) > 0:
        points = points[arg.flatten(), :]
        distance = np.sqrt(np.sum((centre - points)**2, axis=1))
        theta = np.deg2rad(wind_dir) - np.arctan((points -
                                                  centre)[:, 1]/(points - centre)[:, 0])
        width = np.abs(distance*np.sin(theta))
        # C0ppm = concentration_distr(width_triangle, width, concentrations[0])
        # H2ppm = concentration_distr(width_triangle, width, concentrations[1])
        # print(C0ppm[0])
        # print(width,width_triangle/2)
        # print(C0ppm)

        #theta = points[arg]-centre
        # print(theta[:,0])
       # print(centre - points[arg])
      #  return points[arg,:]


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
