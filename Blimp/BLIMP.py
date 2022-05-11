#MASTER Blimp script
import numpy as np
import matplotlib.pyplot as plt
from first_concept import drag,velocity, balloon_mass, surface_area
from propulsion_power import power_calc, read_irradiance
from materials import Cellophane

###################
# Constants
###################

g                               = 9.81  # [N/kg]
rho                             = 1.225  # [kg/m3]
spheroid_ratio                  = 3  # []
foil_thickness                  = 0.000008  # [m]
foil_gsm                        = 11.36  # [g/m2]
linen_light_gsm                 = 30  # [g/m2]
linen_heavy_gsm                 = 150  # [g/m2]
silk_gsm                        = 21.65  # [g/m2]
solar_gsm                 = 0.42  # [g/m2]
p                               = 1.6075  # []
prop_eff                        = 0.8
motor_eff                       = 0.9
toplevel_margin                 = 1.2

dl_re=np.array([[0.05    ,2.36],
                [0.1     ,1.491],
                [0.15    ,1.138],
                [0.182   ,1],
                [0.2     ,0.94],
                [0.25    ,0.81],
                [0.3     ,0.716]
    ])

lift_he                         = 1.0465
lift_h2                          = 1.14125

###################
# Top-level inputs
###################
class Blimp:
    def __init__(self, mass_payload, mass_undercarriage, mass_propulsion, mass_electronics, mass_balloon, mass_solar_cell, mass_ballonet):
        self.mass_payload = mass_payload
        self.mass_undercarriage = mass_undercarriage
        self.mass_propulsion = mass_propulsion
        self.mass_electronics = mass_electronics
        self.mass_balloon = mass_balloon
        self.mass_solar_cell = mass_solar_cell
        self.mass_ballonet = mass_ballonet

        self.mass_total = mass_payload + mass_undercarriage + mass_propulsion + mass_electronics +  mass_balloon + mass_solar_cell + mass_ballonet
        self.volume = self.mass_total/lift_h2

BLIMP = Blimp(mass_payload =       25,        # [kg]
              mass_undercarriage=   3,     # [kg]
              mass_propulsion=      0.8,      # [kg]
              mass_electronics=     1,       # [kg]
              mass_balloon=         0,           # [kg]
              mass_ballonet=        0.75,       # [kg]
              mass_solar_cell=      0)        # [kg]


#Solar panel simulation
alphas = []
vels = []
tmy=read_irradiance()
for alpha in np.arange(0, round(np.pi, 2), 0.01):
    for i in range(200):

        mass_total = BLIMP.mass_payload + BLIMP.mass_undercarriage + BLIMP.mass_propulsion + BLIMP.mass_electronics + BLIMP.mass_balloon + BLIMP.mass_solar_cell + BLIMP.mass_ballonet
        volume = mass_total / lift_h2
        area_balloon, radius, half_length, BLIMP.mass_balloon = balloon_mass(volume, spheroid_ratio, p, silk_gsm, foil_gsm)
        power_solar, area_solar = power_calc(radius,half_length,alpha,0.8, tmy  )
        BLIMP.mass_solar_cell=area_solar*solar_gsm
        D = drag(volume, spheroid_ratio, dl_re, rho, np.arange(1,100,1))
        v_max, v_opt = velocity(power_solar / toplevel_margin, prop_eff, motor_eff, D, np.arange(1,100,1))

    alphas.append(alpha)
    vels.append(v_opt[0])
    print(alpha)
plt.scatter(alphas, vels)
plt.show()