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
    x_sensor_temp = np.arange(0, size+spacing, spacing)
    x_sensor = np.array([x for x in x_sensor_temp if x < size])
    y_sensor_temp = np.arange(0, size+spacing, spacing)
    y_sensor = np.array([y for y in y_sensor_temp if y < size])
    n, m = len(x_sensor), len(y_sensor)
    mesh = np.array(np.vstack(
        map(np.ravel, np.meshgrid(x_sensor, y_sensor))).transpose(), dtype=float)

    for j in range(m):
        if j % 2 == 0:
            mesh[j*n:j*n+n, 0] = mesh[j*n:j*n+n, 0] + shift_perc*spacing

    return mesh


def disply_mesh(subtiles_nbr):
    spacing_sequence = np.random.uniform(300, 470, int(subtiles_nbr**2))
    mesh_arr = []
    for i in range(len(spacing_sequence)):
        mesh_arr.append(mesh1(1500, spacing_sequence[i]))
    # print(mesh_arr)
    for i in range(len(spacing_sequence)):
        for j in range(len(mesh_arr[i])):
            mesh_arr[i][j][0] += 1500*(i % subtiles_nbr)
            mesh_arr[i][j][1] += 1500*(np.floor(i/subtiles_nbr) % subtiles_nbr)
    final_mesh = np.concatenate(mesh_arr)
    return final_mesh


if __name__ == "__main__":
    subtiles_nbr = 4
    size = 1500*subtiles_nbr
    mesh_points = disply_mesh(subtiles_nbr)
    # print(mesh_points)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(mesh_points[:, 0], mesh_points[:, 1])
    plt.xlim(0, size)
    plt.ylim(0, size)
    plt.ylabel("Latitude [m]")
    plt.xlabel("Longitude [m]")
    plt.show()
