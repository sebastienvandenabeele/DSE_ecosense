from simulator import *
import numpy as np
from matplotlib import pyplot as plt

def getRestoringForce(h, blimp):
    delta_rho = getISA('rho', h) - getISA('rho', blimp.h_trim)
    force = -delta_rho * blimp.volume * g       # TODO: adapt volume for ballonets change
    return force

def getK(blimp):
    h1 = blimp.h_trim - 1
    h2 = blimp.h_trim + 1

    k = getRestoringForce(h2, blimp) - getRestoringForce(h1, blimp) / (h1 - h2)
    return k*2



def simulateFlightpath(blimp, ref_path):

    k = 20
    dt = 0.05
    ts = np.arange(0, len(ref_path), dt)

    xs = range(len(ref_path))
    hs = []
    h = 299
    v_y = 0
    for i in range(len(xs)):

        vertical_thrust_req = calculateRestoringForce(h, blimp)
        vertical_thrust = k * (ref_path[i] - h)

        a_y = (vertical_thrust - vertical_thrust_req) / blimp.MTOM
        v_y += a_y * dt
        h += v_y * dt

        hs.append(h)

    plt.plot(xs, blimp.h_trim * np.ones(len(ref_path)), linestyle='dashed', color='black')
    plt.plot(xs, ref_path)
    plt.plot(xs, hs)
    plt.grid
    plt.xlabel('Distance [m]')
    plt.ylabel('Altitude [m]')
    plt.legend(['Trim Altitude', 'Reference Path', 'Actual Path'])
    plt.show()