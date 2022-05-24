import numpy as np


def mesh1(size, x_spacing, y_spacing):
    """Creates a simple recatngular mesh (given x and y spacing)

    Args:
        size (float): size of a side (10x10km for this case) [m]
        x_spacing (float): distance between every points in the x direction
        y_spacing (float): distance between every points in the x direction

    Returns:
        ndarray: returns the mesh in an array of points from left to right and top to bottom
    """
    x_sensor = np.arange(0, size+x_spacing, x_spacing)
    y_sensor = np.arange(0, size+y_spacing, y_spacing)
    return np.vstack(map(np.ravel, np.meshgrid(x_sensor, y_sensor))).transpose()
