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
