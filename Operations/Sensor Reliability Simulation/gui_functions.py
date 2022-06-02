import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Circle, Arc
import matplotlib.animation as animation
import seaborn as sns
import matplotlib.animation as animation
import numpy as np
import simulation_functions as simfunc
import mesh_types
from mpl_toolkits import mplot3d


def concentration_3d(width_triangle, C0_init_ppm, t, lb):
    begin_N = 1
    fig = plt.figure(figsize=(10, 9))
    ax = plt.axes(projection='3d')
    x = np.array([np.linspace(
        width_triangle[0], width_triangle[-1], len(t)), np.linspace(
        width_triangle[0], width_triangle[-1]*lb, len(t))])
    X, Y = np.meshgrid(x[0][begin_N:], x[1][begin_N:])
    data = simfunc.concentration_distribution(x[0][begin_N:])
    Z = np.array([C0_init_ppm[begin_N:]*simfunc.density_plot(x[0][begin_N:],
                 params[0], params[1]) for params in data])
    ax.plot_surface(X, Y, Z, cmap=plt.cm.gist_heat_r)
    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_zlabel('Concentration [ppm]')
    plt.show()
    fig.savefig('./figures/3d_concentration.png')


def animation_2d(width_triangle, C0_init_ppm, t):
    fig, ax = plt.subplots()

    def init():
        sns.heatmap(np.zeros((10, 10)), vmin=0.0, vmax=0.1,
                    cmap="Greys", cbar_kws={'label': 'Concentration [ppm]'})

    def animate(i):
        ax.cla()
        x = np.linspace(
            width_triangle[0], width_triangle[-1], len(t))
        begin_N = 1
        data = simfunc.concentration_distribution(x[begin_N:])
        Z = np.array([C0_init_ppm[i]*simfunc.density_plot(x[begin_N:],
                                                          params[0], params[1]) for params in data])
        c = sns.heatmap(Z, vmin=0.0, vmax=0.1, cmap="Greys", cbar=False)

    anim = animation.FuncAnimation(
        fig, animate, init_func=init, frames=len(t)-1, interval=1, repeat=False)

    anim.save('./figures/2d_animation.gif', writer='imagemagick', fps=60)
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
    fig, ax = plt.subplots(3, figsize=(15, 9))
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
    circle_patch = Circle((x_f+length_triangle[-1]/2 * np.cos(np.deg2rad(wind_dir)), y_f+length_triangle[-1]/2 * np.sin(np.deg2rad(wind_dir))), radius=(length_triangle[-1]/2),

                          facecolor="none", edgecolor="slategrey")
    fig, ax = plt.subplots(figsize=(8, 8))
    for i, ellipse in enumerate(ellipse_patches):
        ax.add_patch(ellipse)
        ax.add_patch(triangle_patches[i])
    ax.add_patch(circle_patch)
    ax.scatter(mesh_points[:, 0], mesh_points[:, 1])
    ax.scatter(relevant_points[:, 0],
               relevant_points[:, 1], color='gold')
    ax.arrow(x_f, y_f, length_triangle[-1]/2 * np.cos(np.deg2rad(
        wind_dir)), length_triangle[-1]/2 * np.sin(np.deg2rad(wind_dir)), width=5, head_width=50, head_length=50, color="black")
    if len(detection_point) != 0:
        ax.scatter(detection_point[:, 0],
                   detection_point[:, 1], color='chartreuse')
    plt.scatter(x_f, y_f, color='red', s=50)
    plt.xlim(0, size)
    plt.xlabel("Longitude [m]")
    plt.ylabel("Latitude [m]")
    plt.ylim(0, size)
    # plt.title(
    #     f'Wind Direction: {np.round(wind_dir, 0)} [deg], Wind Speed: {np.round(wind_spd, 2)} [km/h], Temperature: {np.round(temp, 2)} [C]')
    plt.show()
    fig.savefig('./figures/sensor_patches.png')


def draw_reliability(df):
    fig, ax = plt.subplots(figsize=(15, 9))
    ax.bar(np.arange(36), df["reliability"])
    ax.plot([0, 35], [0.62, 0.62], color='r')
    plt.show()


def draw_overall_reliabilities(x_spacing_rel, y_spacing_rel, shift_rel, x_spacing_range, y_spacing_range, shift_range):
    fig, ax = plt.subplots(3, figsize=(13, 9))
    bar0 = ax[0].bar(x_spacing_range, x_spacing_rel,
                     width=10)
    ax[0].set_xticks(x_spacing_range)
    ax[0].plot(x_spacing_range, [62, 62, 62], '--', color='r')
    ax[0].bar_label(bar0)
    ax[0].set_ylabel("Reliability [%]")
    ax[0].set_xlabel("East-West Sensor Spacing [m]")

    bar1 = ax[1].bar(y_spacing_range, y_spacing_rel,
                     width=10)
    ax[1].set_xticks(y_spacing_range)
    ax[1].plot(y_spacing_range, [62, 62, 62], '--', color='r')
    ax[1].bar_label(bar1)
    ax[1].set_ylabel("Reliability [%]")
    ax[1].set_xlabel("North-South Sensor Spacing [m]")

    bar2 = ax[2].bar(np.array(shift_range)*100, shift_rel,
                     width=3)
    ax[2].set_xticks(np.array(shift_range)*100)
    ax[2].plot(np.array(shift_range)*100, [62, 62, 62], '--', color='r')
    ax[2].bar_label(bar2)
    ax[2].set_ylabel("Reliability [%]")
    ax[2].set_xlabel("Sensor Shift [%]")

    plt.show()


if __name__ == "__main__":
    df = simfunc.read_and_edit_samples("./data/samples.csv")
    t_max = 10*60
    N = int(100*(t_max/(8*60)))
    gas = "CO"
    time = np.linspace(0, t_max, N)
    width_triangle = np.linspace(0, 200, N)
    C0_init_ppm = np.linspace(0, 10, N)
    lb = 1.5
    # animation_2d(width_triangle, C0_init_ppm, time)
    #concentration_3d(width_triangle, C0_init_ppm, time, lb)
