import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Circle
import matplotlib.animation as animation
import seaborn as sns
import matplotlib.animation as animation
import numpy as np
import simulation_functions as simfunc
import mesh_types


def single_animation(mesh, width_triangle, C0_init_ppm, t):
    fig, ax = plt.subplots()

    def init():
        ax.imshow(np.zeros((10, 10)))

    def animate(i):
        ax.cla()
        x = np.linspace(
            width_triangle[0], width_triangle[-1], len(t))
        begin_N = 1

        data = simfunc.concentration_distribution(x[begin_N:])
        Z = np.array([C0_init_ppm[i]*simfunc.density_plot(x[begin_N:],
                                                          params[0], params[1]) for params in data])

        # rotated_Z = ndimage.rotate(Z, 45)
        ax.imshow(Z, vmin=0.0, vmax=0.1, cmap="Greys", zorder=1)
        # ax.scatter(mesh[:, 0], mesh[:, 1], zorder=2)

    anim = animation.FuncAnimation(
        fig, animate, init_func=init, frames=len(t)-1, interval=1, repeat=False)
    plt.show()


def mesh_plot(mesh_points, size, x_spacing, y_spacing, angle):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(mesh_points[:, 0], mesh_points[:, 1])
    plt.xlim(0, size)
    plt.ylim(0, size)
    plt.title(
        f'X spacing: {x_spacing} [m], Y spacing: {y_spacing} [m], Angle: {angle} [deg]')
    plt.show()


def detected_map(mesh_points, df):
    color_dict = dict({True: 'tab:green', False: 'tab:red'})
    fig, ax = plt.subplots(figsize=(8, 8))
    g = sns.scatterplot(x="x_start", y="y_start",
                        hue="detected", palette=color_dict, data=df)
    ax.scatter(mesh_points[:, 0], mesh_points[:, 1])
    plt.show()


def detected_corr(df):
    fig, ax = plt.subplots(3, figsize=(14, 9))
    df[["detected", "wind_dir"]].plot.scatter(
        ax=ax[0], x="wind_dir", y="detected")
    df[["detected", "wind_spd"]].plot.scatter(
        ax=ax[1], x="wind_spd", y="detected")
    df[["detected", "R"]].plot.scatter(
        ax=ax[2], x="R", y="detected")
    plt.show()


def draw_patches(x_f, y_f, centre, length_ellipse, width_ellipse, wind_dir, length_triangle, width_triangle, wind_spd, temp, N, mesh_points, size, detection_point, relevant_points):
    ellipse_patches, triangle_patches = [], []
    for i in range(N):
        ellipse_patches.append(Ellipse((centre[0][i], centre[1][i]), length_ellipse[i],
                                       width_ellipse[i], wind_dir, facecolor="none", edgecolor="orange", linewidth="0.2"))
        triangle_points = simfunc.triangle_points(
            length_triangle[i], width_triangle[i], (centre[0][i], centre[1][i]), wind_dir)
        triangle_patches.append(Polygon(
            triangle_points, closed=True, facecolor="none", edgecolor="grey", linewidth="0.2"))
    circle_patch = Circle((x_f+length_triangle[-1]/2 * np.cos(np.deg2rad(wind_dir)), y_f+length_triangle[-1]/2 * np.sin(np.deg2rad(wind_dir))), radius=length_triangle[-1]/2,

                          facecolor="none", edgecolor="red")
    fig, ax = plt.subplots(figsize=(8, 8))
    for i, ellipse in enumerate(ellipse_patches):
        ax.add_patch(ellipse)
        ax.add_patch(triangle_patches[i])
    ax.add_patch(circle_patch)
    ax.scatter(mesh_points[:, 0], mesh_points[:, 1])
    ax.scatter(relevant_points[:, 0],
               relevant_points[:, 1], color='cyan')
    if len(detection_point) != 0:
        ax.scatter(detection_point[:, 0],
                   detection_point[:, 1], color='chartreuse')
    plt.scatter(x_f, y_f, color='red')
    plt.xlim(0, size)
    plt.ylim(0, size)
    plt.title(
        f'Wind Direction: {np.round(wind_dir, 0)} [deg], Wind Speed: {np.round(wind_spd, 2)} [km/h], Temperature: {np.round(temp, 2)} [C]')
    plt.show()


if __name__ == "__main__":
    df = simfunc.read_and_edit_samples("./data/samples.csv")
    t_max = 8*60
    N = int(100*(t_max/(8*60)))
    gas = "CO"
    time = np.linspace(0, 10*60, N)
    u = 10/3.6
    R = 0.1/3.6
    lb = 1.5
    wind_dir = 20
    temp = 25
    size = 10000
    iteration = [300, 300, 0]
    x_f, y_f = np.random.uniform(0, size, 2)
    mesh_points = mesh_types.mesh1(
        size, iteration[0], iteration[1], iteration[2])
    length_triangle, width_triangle = simfunc.cone_params(time, u, lb)
    length_ellipse, width_ellipse, centre_ellipse = simfunc.ellips_params(
        time, R, lb)
    centre = [x_f+centre_ellipse*np.cos(np.deg2rad(wind_dir)),
              y_f + centre_ellipse*np.sin(np.deg2rad(wind_dir))]
    draw_patches(x_f, y_f, centre, length_ellipse, width_ellipse,
                 wind_dir, length_triangle, width_triangle, u, temp, N, mesh_points, size)
