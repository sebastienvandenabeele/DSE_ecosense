from simulator import *
import numpy as np
from matplotlib import pyplot as plt
import control.matlab as ml

def trim(cruisepath)

def getRestoringForce(h, blimp):
    delta_rho = getISA('rho', h) - getISA('rho', blimp.h_trim)
    force = -delta_rho * blimp.volume * g       # TODO: adapt volume for ballonets change
    return force

def getK(blimp):
    h1 = blimp.h_trim - 1
    h2 = blimp.h_trim + 1

    k = (getRestoringForce(h2, blimp) - getRestoringForce(h1, blimp)) / (h2 - h1)
    return k

def tuneAltitudeDynamics(blimp, cruisepath):
    m = blimp.MTOM
    c = getC(blimp, cruisepath)
    k = getK(blimp)
    s = ml.tf('s')

    H = 1 / (m * s**2 + c*s + k)    # Blimp Altitude Dynamics TF
    ml.sisotool(H)

def setTF(blimp):
    m = blimp.MTOM
    c = getC(blimp, cruisepath)
    k = getK(blimp)
    s = ml.tf('s')

    H = 1 / (m * s ** 2 + c * s + k)  # Blimp Altitude Dynamics TF


def simulateFlightpath(blimp, ref_path):

    k = 20
    dt = 0.05
    ts = np.arange(0, len(ref_path), dt)

    xs = range(len(ref_path))
    hs = []
    h = 299
    v_y = 0
    for i in range(len(xs)):

        vertical_thrust_req = getRestoringForce(h, blimp)
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

def ddx(list):
    return [list[i] - list[i-1] for i in np.arange(1, len(list))]

def getC(blimp, cruisepath):
    slope = ddx(cruisepath)
    v_y = np.array([s * blimp.cruiseV for s in slope])
    v_model = np.mean(v_y)

    c = getISA('rho', blimp.h_trim) * blimp.ref_area * v_model * 0.06

    return c
    # diffs = []
    # vs = np.arange(min(v_y), max(v_y), 0.001)
    # for v in vs:
    #     diffs.append(sum(np.abs(v_y - v)))
    # v_model = vs[np.argwhere(diffs == min(diffs))][0][0]
    # return v_model




# v_avg = np.mean(v_y)
# print(v_model)
# print(v_avg)



#plt.plot(np.arange(len(cruisepath)), cruisepath)
# plt.plot(np.arange(len(v_y)), v_y)
# plt.plot(np.arange(len(v_y)), np.ones(len(v_y)) * v_model)
# plt.legend(['Vertical Velocities', 'Chosen Model Speed'])
# # plt.plot(np.arange(len(elevation)), elevation)
# # plt.plot(np.arange(len(elevation_ma)), elevation_ma)
# plt.grid()
# # plt.legend(['Height', 'Elevation', 'Elevation MA'])
# plt.show()