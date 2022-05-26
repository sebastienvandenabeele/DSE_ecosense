def calculateAltitudeGain(blimp):
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