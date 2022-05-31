import numpy as np
import matplotlib.pyplot as plt


def mesh1(size, spacing, shift_perc=0):
    """Creates a simple recatngular mesh (given x and y spacing)

    Args:
        size (float): size of a side (10x10km for this case) [m]
        x_spacing (float): distance between every points in the x direction
        y_spacing (float): distance between every points in the x direction

    Returns:
        ndarray: returns the mesh in an array of points from left to right and top to bottom
    """
    x_sensor = np.arange(0, size+spacing, spacing)
    y_sensor = np.arange(0, size+spacing, spacing)
    n, m = len(x_sensor), len(y_sensor)
    mesh = np.array(np.vstack(
        map(np.ravel, np.meshgrid(x_sensor, y_sensor))).transpose(), dtype=float)

    for j in range(m):
        if j % 2 == 0:
            mesh[j*n:j*n+n, 0] = mesh[j*n:j*n+n, 0] + shift_perc*spacing

    return mesh


if __name__ == "__main__":
    size = 10
    mesh_points = mesh1(size, 2, shift_perc=0.75)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(mesh_points[:, 0], mesh_points[:, 1])
    plt.xlim(0, size)
    plt.ylim(0, size)
    plt.show()
