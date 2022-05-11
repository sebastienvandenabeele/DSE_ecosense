#MASTER Blimp script
import numpy as np
import matplotlib.pyplot as plt
import solarcells as sc
from first_concept import drag,velocity, balloon_mass, surface_area
from propulsion_power import power_calc, read_irradiance

###################
# Constants
###################

#Physical Constants
lift_he                         = 1.0465
lift_h2                          = 1.14125
g                               = 9.81  # [N/kg]
rho                             = 1.225  # [kg/m3]

dl_re=np.array([[0.05    ,2.36],
                [0.1     ,1.491],
                [0.15    ,1.138],
                [0.182   ,1],
                [0.2     ,0.94],
                [0.25    ,0.81],
                [0.3     ,0.716]
    ])


spheroid_ratio                  = 3  # []
foil_density                    = 0.01136  # [kg/m2]
linen_light_density             = 0.030  # [kg/m2]
linen_heavy_density             = 0.150  # [kg/m2]
silk_density                    = 0.02165  # [kg/m2]
p                               = 1.6075  # []
prop_eff                        = 0.8
motor_eff                       = 0.9
prop_limit                      = 0.75





###################
# Requirement inputs
###################
toplevel_margin                 = 1.2
maximum_triptime                = 2 * 3600  # [given in h, processed in s]
range                           = 300000    # [m]
minimum_velocity                = range / maximum_triptime


#Environment
avg_sun_elevation = 52  # [deg]
tmy = read_irradiance()


class Blimp:
    def __init__(self, mass_payload, mass_undercarriage, mass_propulsion,
                 mass_electronics, mass_ballonet, solar_cell, length_factor, spheroid_ratio,
                 mass_solar_cell=0, mass_balloon=0, panel_angle=0):

        #Solar cells
        self.solar_cell = solar_cell
        self.panel_angle = panel_angle
        self.length_factor = length_factor


        #Balloon Aerodynamics
        self.spheroid_ratio = spheroid_ratio
        dl = 1 / spheroid_ratio
        ld = spheroid_ratio
        list_element = min(dl_re[:, 0], key=lambda x: abs(x - dl))
        re = dl_re[np.where(dl_re[:, 0] == list_element), 1][0][0]
        self.CD = (0.172 * ld ** (1 / 3) + 0.252 * dl ** 1.2 + 1.032 * dl ** 2.7) / ((re * 10 ** 7) ** (1 / 6))



        #Masses
        self.mass_payload = mass_payload
        self.mass_undercarriage = mass_undercarriage
        self.mass_propulsion = mass_propulsion
        self.mass_electronics = mass_electronics
        self.mass_balloon = mass_balloon
        self.mass_solar_cell = mass_solar_cell
        self.mass_ballonet = mass_ballonet
        self.mass_total = mass_payload + mass_undercarriage + mass_propulsion + mass_electronics +  mass_balloon + mass_solar_cell + mass_ballonet

        self.volume = self.mass_total/lift_h2



    def sizeSolar(self):
        self.area_solar = 0.8 * 2 * self.length / 2 * self.radius * 2 * self.panel_angle
        minimum_area = 2 * np.sin(self.panel_angle) * self.radius * self.length_factor * 2 * self.length / 2 * np.cos(avg_sun_elevation)
        # maximum_area = (1 - np.cos(avg_sun_elevation + self.panel_angle)) * self.radius * 0.8 * 2 * self.length / 2

        power_max = minimum_area * np.mean(tmy["DNI"]) + np.mean(tmy["DHI"]) * self.area_solar
        self.power_solar = power_max * self.solar_cell.efficiency * self.solar_cell.fillfac


    def sizeBalloon(self):
        self.radius = ((3 * self.volume) / (4 * self.spheroid_ratio)) ** (1 / 3)
        self.length = self.spheroid_ratio * self.radius * 2
        self.surface_area = 4*np.pi * ((self.radius**(2*p) + 2*(self.radius*self.length/2)**p)/3)**(1/p)
        self.mass_balloon = self.surface_area * (silk_density + foil_density)





    def setCruiseSpeed(self, v_target, plot=False):
        print('designing Blimp for cruise speed of ', v_target, 'm/s')
        alphas = []
        vs = []
        vols = []
        masses = []
        for alpha in np.arange(0, np.radians(180), 0.01):
            print(alpha)
            self.panel_angle = alpha
            for i in np.arange(0, 200, 1):
                self.mass_total = self.mass_payload + self.mass_undercarriage + self.mass_propulsion + self.mass_electronics + self.mass_balloon + self.mass_solar_cell + self.mass_ballonet
                self.volume = self.mass_total / lift_h2
                self.sizeBalloon()
                self.sizeSolar()
                self.mass_solar_cell = self.area_solar * self.solar_cell.density
                self.ref_area = self.volume**(2/3)
                self.cruiseV = (2 * self.power_solar * prop_eff * motor_eff * prop_limit / toplevel_margin / rho / self.ref_area / self.CD)**(1/3)

            if plot:
                alphas.append(alpha)
                vs.append(self.cruiseV)
                vols.append(self.volume)
                masses.append(self.mass_total)
            print('volume [m3]: ', self.volume)
            print('mass [kg]: ', self.mass_total)
            print('velocity [m/s]: ', self.cruiseV)
            if self.cruiseV >= v_target: break

        if plot:
                plt.scatter(alphas, vs)
                plt.scatter(alphas, vols)
                plt.scatter(alphas, masses)
                plt.legend(['Velocity', 'Volume', 'Mass'])
                plt.show()

########################### END OF CLASS DEF ############################### END OF CLASS DEF #######################################



#Blimp Initialisation
Shlimp = Blimp(mass_payload =       25,  # [kg]
               mass_undercarriage=   3,  # [kg]
               mass_propulsion=      0.8,  # [kg]
               mass_electronics=     1,  # [kg]
               mass_ballonet=        0.75,  # [kg]
               length_factor=       0.8,
               spheroid_ratio=      3,
               solar_cell=sc.maxeon_gen3)

Shlimp.setCruiseSpeed(minimum_velocity, True)





