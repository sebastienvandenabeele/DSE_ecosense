from matplotlib import pyplot as plt
import numpy as np
import requirements as req
from solar_sizing import projectPanel, getIrradiance
import BLIMP as Blimp

rho = 1.225
T0 = 288.15             # [K]
p0 = 101325             # [Pa]
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

def simulateRange(blimp):
    start_time = 9      # [h]
    end_time = 16
    hours = np.arange(start_time, end_time+1, 1)
    elevations = [23, 34, 45, 53, 56, 55, 48, 38, 26, 14]  # [deg] starts at 8 ends at 17

    #range = 0
    vs = []
    powers = []
    for t in hours:
        print('Its', t, 'o clock')
        elevation = elevations[t - 8]
        total_area, shone_area = projectPanel(blimp, elevation, 30)
        tmy = getIrradiance(t, t)
        DNI = np.mean(tmy['DNI'])
        DHI = np.mean(tmy['DHI'])

        generated_power = (DNI * shone_area + DHI * total_area) * blimp.solar_cell.efficiency * blimp.solar_cell.fillfac
        powers.append(generated_power)
        installed_power = blimp.n_engines * blimp.engine.max_power * Blimp.prop_limit
        power_for_prop = generated_power - blimp.power_electronics
        gross_prop_power = min(power_for_prop, installed_power)
        net_prop_power = gross_prop_power * blimp.engine.efficiency * Blimp.prop_eff

        v = (2 * net_prop_power / (blimp.ref_area * blimp.CD * Blimp.rho))**(1/3)
        vs.append(v)

    design_range = blimp.cruiseV * (end_time - start_time) * 3.6
    simrange = np.mean(vs) * 3.6 * (end_time - start_time)
    print('Simulated range:', simrange)
    print('Design Range:', design_range)
    plt.scatter(hours, vs)
    plt.plot(hours, np.ones(len(hours)) * blimp.cruiseV, linestyle='dashed')
    # plt.scatter(hours, powers, color='yellow')
    # plt.plot(hours, np.ones(len(hours)) * blimp.generated_power, color='yellow')
    plt.xlabel('Time [h]')
    plt.ylabel('Velocity [m/s]')

    plt.grid()
    plt.show()

print()


def simPower(blimp):
    global power_required
    dt = 20 # min
    ts = np.arange(9 * 60, 16 * 60, dt)
    generated_powers = []
    times = []

    E = 0

    elevations = []
    shone_areas = []
    total_areas = []


    for t in ts:
        hour = t//60
        minute = t % 60
        time = hour + minute/60

        print('Its', hour, ':', minute, '/ ', time)
        elevation = -2 * time**2 + 49 * time -244
        elevations.append(elevation)
        print('Sun elevation:', elevation, 'deg')

        total_area, shone_area = projectPanel(blimp, elevation, 30)
        total_areas.append(total_area)
        shone_areas.append(shone_area)
        tmy = getIrradiance(hour, hour)
        DNI = np.mean(tmy['DNI'])
        DHI = np.mean(tmy['DHI'])

        generated_power = (DNI * shone_area + DHI * total_area) * blimp.solar_cell.efficiency * blimp.solar_cell.fillfac
        generated_powers.append(generated_power)
        print('Power generated', generated_power, 'W')

        power_required = (blimp.power_for_prop + blimp.power_electronics)

        times.append(time)


    usedpowers = power_required * np.ones(len(ts))

    generated_energy = 0
    used_energy = 0
    for power in generated_powers:
        generated_energy += power * dt * 60
    for power in usedpowers:
        used_energy += power * dt * 60

    print('Total Generated Energy [J] ', generated_energy)
    print('Total Used Energy [J]', used_energy)

    print(E)
    plt.plot(times, usedpowers)
    plt.scatter(times, generated_powers)
    plt.xlabel('Time [h]')
    plt.ylabel('Power [W]')
    plt.grid()
    plt.legend(['Power Required', 'Power Available'])
    plt.show()







