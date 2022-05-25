import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
import matplotlib.animation as animation
import seaborn as sns
import matplotlib.animation as animation
import numpy as np
import simulation_functions as simfunc

def single_animation(width_triangle, C0_init_ppm, N, t):
    fig = plt.figure()

    def init():
        sns.heatmap(np.zeros((10, 10)), vmax=.8,
                    square=True, cbar=False)

    def animate(i):
        plt.clf()
        x = np.linspace(
            width_triangle[0], width_triangle[-1], len(t))
        begin_N = 1
        data = simfunc.concentration_distribution(x[begin_N:])
        Z = np.array([C0_init_ppm[i+begin_N]*simfunc.density_plot(x[begin_N:],
                                                            params[0], params[1]) for params in data])
        sns.heatmap(Z, vmin=0.0, vmax=0.05, cmap="Greys")

    anim = animation.FuncAnimation(
        fig, animate, init_func=init, frames=N-1, interval=10, repeat=False)

    plt.show()


def mesh_plot(mesh_points, size, x_spacing, y_spacing, angle):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(mesh_points[:, 0], mesh_points[:, 1])
    plt.xlim(0, size)
    plt.ylim(0, size)
    plt.title(
        f'X spacing: {x_spacing} [m], Y spacing: {y_spacing} [m], Angle: {angle} [deg]')
    plt.show()
