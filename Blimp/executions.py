import numpy as np
from matplotlib import pyplot as plt
from BLIMP import *


maximum_triptime                = 5 * 3600  # [s]
minimum_velocity                = req.range / maximum_triptime

REQ_n_sensors                   = 1295 / 2
relays_per_sensor               = 25
n_relays                        = int(round(REQ_n_sensors / relays_per_sensor, 0))
m_sensor                        = 0.052      # [kg]
m_relay                         = 0.338     # [kg]
m_deployment_system             = 2         # [kg]
REQ_payload_mass                = n_relays * m_relay + REQ_n_sensors * m_sensor + m_deployment_system

flightdata = np.genfromtxt('flight_path.csv', delimiter=',', skip_header=1)
path = flightdata[:, 0]
cruisepath = path[194:-194]
trim_altitude = np.mean(cruisepath)




#Creation of blimp design, run either this or unpickle from file
Shlimp = Blimp(name=                "Shlimp_0106_1031",
               mass_payload =       REQ_payload_mass,
               target_speed=        minimum_velocity,
               mass_deployment=      15,
               n_fins=           4,

               envelope_material=    mat.polyethylene_fiber,
               balloon_pressure=     500,
               h_trim=               trim_altitude,
               n_engines=            2,
               engine=              eng.tmt_4130_300,

               electronics=         el.config_option_1,
               length_factor=        0.9,
               spheroid_ratio=       3,
               liftgas=             gas.hydrogen,
               solar_cell=          solar.maxeon_gen3)


# #Shlimp = unpickle('Shlimp_no_alt_ctrl')
# # simAltitudeDynamics(Shlimp, cruisepath)
#
Shlimp.report()
Shlimp.estimateCost()
Shlimp.save()

# hs = np.arange(Shlimp.h_trim-3000, Shlimp.h_trim + 3000, 1)
# fs = [getRestoringForce(h, Shlimp) for h in hs]
# fs_linearised = getK(Shlimp) * (hs - Shlimp.h_trim)
# plt.plot(hs, fs, linestyle='dashed')
# plt.plot(hs, fs_linearised)
# plt.xlim(Shlimp.h_trim-3000,Shlimp.h_trim+ 3000)
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
