import numpy as np
from matplotlib import pyplot as plt
from BLIMP import *
from gondola import *


maximum_triptime                = 7 * 3600  # [s]
minimum_velocity                = req.range / maximum_triptime

REQ_n_sensors                   = int(round(1295 / 2, 0))
relays_per_sensor               = 25
n_relays                        = int(round(REQ_n_sensors / relays_per_sensor, 0))
m_sensor                        = 0.052      # [kg]
m_relay                         = 0.338     # [kg]
REQ_payload_mass                = n_relays * m_relay + REQ_n_sensors * m_sensor

flightdata = np.genfromtxt('flight_path_data.csv', delimiter=',', skip_header=1)
altitude_path = flightdata[:, 2]

cruisepath = altitude_path[260:-240]


trim_altitude = np.mean(cruisepath)

gondola = Gondola(length=2, height=0.5, x=-1, z=-2)


#Creation of blimp design, run either this or unpickle from file
Shlimp = Blimp(name=                "Shlimp_for_model",
               mass_payload =       REQ_payload_mass,
               target_speed=        minimum_velocity,
               mass_deployment=      15,
               n_fins=                4,
               gondola=             gondola,

               envelope_material=    mat.polyethylene_fiber,
               balloon_pressure=     500,
               h_trim=               trim_altitude,
               n_engines=            4,
               n_engines_rod=        1,
               engine=              eng.tmt_4130_300,
               d_eng=                2,

               gondola_electronics=  el.config_option_1,
               length_factor=        0.9,
               spheroid_ratio=       3,
               liftgas=             gas.hydrogen,
               solar_cell=          solar.maxeon_gen3)


# Shlimp = unpickle('Shlimp_for_model')
Shlimp.report()
Shlimp.estimateCost()
Shlimp.save()
symStateSpace(Shlimp)


# Shlimp.h_trim = 250
# print(getISA('p', 0))
# print(getISA('p', 250))
# print(getISA('p', 500))
# print()
# print(getISA('rho', 0))
# print(getISA('rho', 250))
# print(getISA('rho', 500))
# print()
# print(getK(Shlimp) * 250)
# print(getK(Shlimp) * -250)


# simulateRange(Shlimp)

# simAltitudeDynamics(Shlimp, cruisepath)
# vys = np.arange(-20, 20, 1)
# fs = [0.5 * getISA('rho', Shlimp.h_trim) * np.sqrt(vy**2 + Shlimp.cruiseV**2) * vy * Shlimp.ref_area * Shlimp.CD for vy in vys]
# fs_linearised = getC(Shlimp, cruisepath) * vys
# plt.plot(vys, fs, linestyle='dashed')
# plt.plot(vys, fs_linearised)
# plt.xlim((-20, 20))
# plt.legend(['Usual Drag Model', 'Small Angle Approximation'])
# plt.grid()
# plt.xlabel('Vertical Velocity [m/s]')
# plt.ylabel('Drag in Vertical Direction [N]')
# plt.show()

# dhs = np.arange(-2000, 2000, 1)
# fs = [getRestoringForce(dh, Shlimp) for dh in dhs]
# fs_linearised = getK(Shlimp) * dhs
# plt.plot(dhs, fs, linestyle='dashed')
# plt.plot(dhs, fs_linearised)
# plt.xlim(-2000, 2000)
# plt.xlabel('Deviation from Trim Altitude [m]')
# plt.ylabel('Buoyancy Restoring Force [N]')
# plt.legend(['ISA Model', 'ISA Model (linearised)'])
# plt.grid()
# plt.show()


# Control Simulation
# xs = np.arange(5000)
# ref_path = 10 * np.sin(0.01* xs) + 300
# simulateFlightpath(Shlimp, ref_path, 300)


# Shlimp.estimateCost()
#simulateCruiseAcceleration(Shlimp)
#simulateVelocity(Shlimp, v0=Shlimp.cruiseV, throttle=0, tmax=50)
#Shlimp.report()
#plot_blimp(Shlimp)
