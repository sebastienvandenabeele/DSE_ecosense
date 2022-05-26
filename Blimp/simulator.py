from matplotlib import pyplot as plt
import numpy as np
import requirements as req

rho = 1.225
T0 = 288.15             # [K]
p0 = 103125             # [Pa]
rho0 = 1.225            # [kg/m^3]
g = 9.81                # [m/s^2]
R = 287                 # [J/kg/K]
lapse_rate = -0.0065    # [K/m]
e = - g / lapse_rate / R

def getISA(key, h):
    """
    International Standard Atmosphere calculations for troposphere layer
    :param key: [str] what parameter should be returned
    :param h: [float] altitude from 0 to 11000 [m]
    :return: [float] altitude parameter chosen by :param: key
    """
    if h > 11000: print('WARNING: Altitude outside of troposphere entered!')
    h = min(h, 11000)

    ISA = {}
    ISA['T'] = T0 + lapse_rate * h                  # [K]
    ISA['p'] = p0 * (ISA['T'] / T0) ** e            # [Pa]
    ISA['rho'] = rho0 * (ISA['T'] / T0) ** (e - 1)  # [kg/m^3]

    return ISA[key]

def simulateCruiseAcceleration(blimp, v0=0, throttle=1, tmax=30):
    """
    :param blimp: Instance of blimp class used for acceleration simulation
    :param v0: Initial velocity of blimp
    :param throttle: Throttle factor multiplied with steady-state power available
    :param tmax: simulation time
    """

    vs = [v0]
    ts = [0]
    v = 0
    E = 0.5 * v0 ** 2 * blimp.MTOM
    dt = 0.1
    for t in np.arange(0, tmax, dt):
        v = np.sqrt(2 * E / blimp.MTOM)
        dP = blimp.prop_power_available * throttle - 0.5 * rho * v ** 3 * blimp.ref_area * blimp.CD
        E += dP * dt

        ts.append(t)
        vs.append(v)

    plt.plot(ts, vs)
    plt.plot(ts, blimp.cruiseV * np.ones(len(ts)), linestyle='dashed', color='black')
    plt.grid()
    plt.xlim(0, tmax)
    plt.ylim(0, req.min_cruiseV * 1.2)
    plt.legend(['Current velocity', 'Design velocity'])
    plt.xlabel('Time [s]')
    plt.ylabel('Velocity [m/s]')
    # plt.savefig('acceleration.png')
    plt.show()


def simulateTurn(blimp):

    print()








