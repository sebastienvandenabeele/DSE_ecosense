from matplotlib import pyplot as plt
import numpy as np
import requirements as req

rho = 1.225

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

def simulateAltitudeGain(blimp):
    lapse_rate = -0.0065  # K/m
    R = 287
    g = 9.81
    e = -g / lapse_rate / R - 1

    # Starting conditions (300m above SL)
    rho0 = 1.19  # kg/m^3
    T0 = 286.2  # K

    V = blimp.volume
    delta_m = -blimp.mass['payload']
    delta_rho_atm = delta_m / V
    rho1 = rho0 + delta_rho_atm

    T1 = T0 * (rho1/rho0)**(1/e)
    delta_T = T1 - T0
    delta_h = delta_T / lapse_rate
    print('Required altitude gain to maintain equilibrium after dropping all payload: ', int(round(delta_h, 0)), ' m')


