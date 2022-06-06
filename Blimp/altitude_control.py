from simulator import *
import numpy as np
from matplotlib import pyplot as plt
import control.matlab as ml

xstep = 200  # [m]

def setLiftConstant(altitude, delta_p):
    rho_atm = getISA('rho', altitude)

    p = getISA('p', altitude) + delta_p
    T = getISA('T', altitude)
    R = 8.314
    M = 0.00201568
    rho_gas = p * M / (R * T)

    return rho_atm - rho_gas

def getRestoringForce(delta_h, blimp):
    delta_rho = getISA('rho', blimp.h_trim) - getISA('rho', blimp.h_trim + delta_h)
    force = delta_rho * blimp.volume * g       # TODO: adapt volume for ballonets change
    return force

def getK(blimp):
    h1 = - 1
    h2 = 1

    k = (getRestoringForce(h2, blimp) - getRestoringForce(h1, blimp)) / (h2 - h1)
    return k

def simAltitudeDynamics(blimp, cruisepath):
    m = blimp.MTOM
    c = getC(blimp, cruisepath)
    k = getK(blimp)
    s = ml.tf('s')

    kp = 2 # Proportional Control Gain

    ref_signal = cruisepath - blimp.h_trim

    OLTF = kp / (m * s**2 + c*s + k)    # Blimp Altitude Dynamics TF
    CLTF = OLTF / (1 + OLTF)           # Unit feedback closed-loop TF
    sys = ml.ss(CLTF)
    ts = np.arange(0, len(cruisepath) * xstep / blimp.cruiseV, xstep / blimp.cruiseV)

    #ys, ts, xs = ml.lsim(sys, U=ref_signal, T = ts, X0=ref_signal[0])

    hs, forces, thetas, gammas = simNonLinear(blimp, ref_signal, ts, kp)
    alphas = thetas - gammas

    plt.subplot(321)
    plt.plot(ts, hs + blimp.h_trim)
    plt.plot(ts, ref_signal + blimp.h_trim)
    plt.plot(ts, blimp.h_trim * np.ones(len(ts)), linestyle='dashed', color='black')
    plt.grid()
    plt.xlabel('Time [s]')
    plt.ylabel('Altitude [m]')
    plt.legend(['Non-Linear Simulation', 'Reference Flightpath', 'Trim Altitude'])

    plt.subplot(322)
    plt.plot(ts, forces)
    plt.grid()
    plt.xlabel('Time [s]')
    plt.ylabel('Force required [N]')

    plt.subplot(323)
    plt.plot(ts, thetas * 57.3)
    plt.grid()
    plt.xlabel('Time [s]')
    plt.ylabel('Pitch angle [deg]')

    plt.subplot(324)
    plt.plot(ts, gammas * 57.3)
    plt.grid()
    plt.xlabel('Time [s]')
    plt.ylabel('Flightpath angle [deg]')

    plt.subplot(325)
    plt.plot(ts, alphas * 57.3)
    plt.grid()
    plt.xlabel('Time [s]')
    plt.ylabel('Angle of attack [deg]')

    plt.show()

def simNonLinear(blimp, ref_path, ts, kp):

    h = ref_path[0]
    v = 0

    hs = []
    forces = []
    thetas = []
    gammas = []
    dt = ts[1] - ts[0]
    vertical_thrust_effectiveness = 1 + blimp.cruise_thrust * blimp.d_eng / (blimp.MTOM * g * blimp.z_cg)

    for i in range(len(ts)):
        hs.append(h)

        e = ref_path[i] - h
        u = kp * e
        force_required = u / vertical_thrust_effectiveness
        forces.append(force_required)
        thetas.append(np.arcsin(force_required * blimp.d_eng / (blimp.MTOM * g * blimp.z_cg)))
        gammas.append(np.arctan(v / blimp.cruiseV))
        v_vec = np.sqrt(v**2 + blimp.cruiseV**2)
        drag_vec = 0.5 * getISA('rho', h) * v_vec**2 * blimp.ref_area * blimp.CD
        drag_vert = drag_vec * v / v_vec

        Fnet = u + getRestoringForce(h, blimp) - drag_vert

        a = Fnet / blimp.MTOM

        v += a * dt
        h += v * dt


    return np.array(hs), np.array(forces), np.array(thetas), np.array(gammas)



    #     vertical_thrust_req = getRestoringForce(h, blimp)
    #     vertical_thrust = k * (ref_path[i] - h)
    #
    #     a_y = (vertical_thrust - vertical_thrust_req) / blimp.MTOM
    #     v_y += a_y * dt
    #     h += v_y * dt
    #
    #     hs.append(h)
    #
    # plt.plot(xs, blimp.h_trim * np.ones(len(ref_path)), linestyle='dashed', color='black')
    # plt.plot(xs, ref_path)
    # plt.plot(xs, hs)
    # plt.grid
    # plt.xlabel('Distance [m]')
    # plt.ylabel('Altitude [m]')
    # plt.legend(['Trim Altitude', 'Reference Path', 'Actual Path'])
    # plt.show()


def ddx(list):
    return [(list[i] - list[i-1])/xstep for i in np.arange(1, len(list))]

def getC(blimp):
    #slope = ddx(cruisepath)
    #v_y = np.array([s * blimp.cruiseV for s in slope])
    #v_model = np.mean(v_y)

    c = 0.5 * getISA('rho', blimp.h_trim) * blimp.cruiseV * blimp.ref_area * blimp.CD

    return c


def symStateSpace(blimp):
    blimp.fin.AR = 3

    V = blimp.cruiseV
    dyn_pressure = 0.5 * getISA('rho', blimp.h_trim) * V**2
    S = blimp.ref_area
    C_m_q_hat = -0.073 # from Blibble, based on Solar HALE
    T1 = blimp.cruise_thrust / 2
    I_yy = blimp.Iyy
    k_atm = getK(blimp)
    c_atm = getC(blimp)
    l_ref  = blimp.volume**(1/3)

    # Moment Arms
    x_ac = blimp.length / 4   # Assumed at quarter length
    z_cg = - blimp.z_cg
    x_fin = (blimp.x_l_fins - 0.5) * blimp.length
    d_eng = blimp.d_eng

    # Coefficients for model
    C_w    = blimp.MTOM * g / (dyn_pressure * S)
    C_m_q  = C_m_q_hat * l_ref / V
    C_T1   = T1 / (dyn_pressure * S)
    K_yy   = I_yy / (dyn_pressure * S * l_ref)
    C_k    = k_atm / (dyn_pressure * S)
    C_mtom = blimp.MTOM / (dyn_pressure * S)
    C_c    = c_atm / (dyn_pressure * S)
    C_L_a_e = 2 / blimp.spheroid_ratio
    C_L_a_h = 2 * blimp.fin.AR * np.pi * blimp.fin.surface / blimp.ref_area

    C_m_a = C_L_a_e * x_ac / l_ref - C_L_a_h * x_fin / l_ref - C_w * z_cg / l_ref
    print('Static stability, CMalpha = ', C_m_a)

    C1 = np.array([[0, 0, -K_yy, 0, 0],
                  [-1, 0, 0, 0, -1/V],
                  [0, 1, 0, 0, 0],
                  [0, 0, 0, 0, -C_mtom],
                  [0, 0, 0, 1, 0]])

    C2 = np.array([[C_L_a_e * x_ac / l_ref - C_L_a_h * x_fin / l_ref, -C_w * z_cg / l_ref, C_m_q, 0, 0],
                   [0, 0, 1, 0, 0],
                   [0, 0, -1, 0, 0],
                   [C_L_a_e + C_L_a_h, 0, 0, -C_k, -C_c],
                   [0, 0, 0, 0, -1]])

    C3 = np.array([[C_T1 * d_eng / l_ref],
                  [0],
                  [0],
                  [C_T1],
                  [0]])

    A = -np.linalg.inv(C1) @ C2  # State Matrix
    B = -np.linalg.inv(C1) @ C3  # Feedback Matrix
    C = np.eye(5)        # Output Matrix
    D = np.zeros([5, 1])            # Feedthrough matrix

    sys = ml.ss(A, B, C, D)
    ml.damp(sys)

    ts = np.arange(0, 30, 0.1)
    us = np.ones(len(ts)) * np.radians(12)

    ys, ts_, xs = ml.lsim(sys, us, ts)

    plt.subplot(326)
    plt.plot(ts, ys[:, 0] * 57.3)
    plt.grid()
    plt.xlabel('Time [s]')
    plt.ylabel('Angle of Attack [deg]')

    plt.subplot(322)
    plt.plot(ts, ys[:, 1] * 57.3)
    plt.grid()
    plt.xlabel('Time [s]')
    plt.ylabel('Pitch Angle [deg]')

    plt.subplot(325)
    plt.plot(ts, ys[:, 2] * 57.3)
    plt.grid()
    plt.xlabel('Time [s]')
    plt.ylabel('Pitch Rate [deg/s]')

    plt.subplot(321)
    plt.plot(ts, ys[:, 3] + blimp.h_trim)
    plt.plot(ts, blimp.h_trim * np.ones(len(ts)), linestyle='dashed', color='black')
    plt.grid()
    plt.xlabel('Time [s]')
    plt.ylabel('Altitude [m]')

    plt.subplot(323)
    plt.plot(ts, ys[:, 4] * 3.6)
    plt.grid()
    plt.xlabel('Time [s]')
    plt.ylabel('Vertical Velocity [km/h]')

    plt.subplot(324)
    plt.plot(ts, ys[:, 4] / V * 57.3)
    plt.grid()
    plt.xlabel('Time [s]')
    plt.ylabel('Flightpath Angle [deg]')

    plt.show()