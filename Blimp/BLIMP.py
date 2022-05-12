#MASTER Blimp script
import numpy as np
import matplotlib.pyplot as plt
from mayavi.mlab import *
import solarcells as sc
import gas
from first_concept import drag,velocity, balloon_mass, surface_area
from propulsion_power import power_calc, read_irradiance
from projected_panel import plot_blimp, irradiance_distribution

###################
# Constants
###################

#Physical Constants
lift_he                         = 1.0465
lift_h2                          = 1.14125
g                               = 9.81  # [N/kg]
p                               = 1.6075  # []

dl_re=np.array([[0.05, 2.36],
                [0.1, 1.491],
                [0.15, 1.138],
                [0.182, 1],
                [0.2, 0.94],
                [0.25, 0.81],
                [0.3, 0.716]
    ])


foil_density                    = 0.01136  # [kg/m2]
linen_light_density             = 0.030  # [kg/m2]
linen_heavy_density             = 0.150  # [kg/m2]
silk_density                    = 0.02165  # [kg/m2]

prop_eff                        = 0.8
motor_eff                       = 0.9
prop_limit                      = 0.75

#Environment
avg_sun_elevation               = 52  # [deg]
tmy = read_irradiance()
rho                             = 1.225  # [kg/m3]




###################
# Requirement inputs
###################
margin                          = 1.2
maximum_triptime                = 5 * 3600  # [given in h, processed in s]
range                           = 300000    # [m]
minimum_velocity                = range / maximum_triptime

n_sensors                       = 1300
relays_per_sensor               = 25
n_relays                        = int(round(n_sensors/relays_per_sensor, 0))
m_sensor                        = 0.05      # [kg]
m_relay                         = 0.338     # [kg]
m_deployment_system             = 2         # [kg]
REQ_payload_mass                = n_relays * m_relay + n_sensors * m_sensor + m_deployment_system

REQ_max_radius                  = 40        # [m]
REQ_max_length                  = 200       # [m]
REQ_max_explosive               = 100000 * 1000 * 1000     # [J] TBD




class Blimp:
    def __init__(self, mass_payload, mass_undercarriage, mass_propulsion, liftgas,
                 mass_electronics, mass_ballonet, solar_cell, length_factor, spheroid_ratio, n_engines,
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
        self.CD = (0.172 * ld ** (1 / 3) + 0.252 * dl ** 1.2 + 1.032 * dl ** 2.7) / ((re * 10 ** 7) ** (1 / 6)) * margin
        self.liftgas = liftgas


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
        self.n_engines = n_engines


    def sizeSolar(self):
        self.area_solar = 0.8 * 2 * self.length / 2 * self.radius * 2 * self.panel_angle
        minimum_area = 2 * np.sin(self.panel_angle) * self.radius * self.length_factor * 2 * self.length / 2 * np.cos(avg_sun_elevation)
        # maximum_area = (1 - np.cos(avg_sun_elevation + self.panel_angle)) * self.radius * 0.8 * 2 * self.length / 2
        minimum_area=self.area_solar*irradiance_distribution(self,avg_sun_elevation)
        # print(irradiance_distribution(self,avg_sun_elevation))
        power_max = minimum_area * np.mean(tmy["DNI"]) + np.mean(tmy["DHI"]) * self.area_solar
        self.power_solar = power_max * self.solar_cell.efficiency * self.solar_cell.fillfac

    def sizeBalloon(self):
        self.radius = ((3 * self.volume) / (4 * self.spheroid_ratio)) ** (1 / 3)
        self.length = self.spheroid_ratio * self.radius * 2
        self.surface_area = 4*np.pi * ((self.radius**(2*p) + 2*(self.radius*self.length/2)**p)/3)**(1/p)
        self.mass_balloon = self.surface_area * (silk_density + foil_density)

    def report(self):
        print('###################### DESIGN CHARACTERISTICS ###################################')
        print()
        print('Number of sensors: ', n_sensors)
        print('Number of relays: ', n_relays)
        print()
        print('MTOM: ', round(self.mass_total, 3), ' kg')
        print('     Solar panel mass: ', round(self.mass_solar_cell, 3), ' kg')
        print('     Balloon mass: ', round(self.mass_balloon, 3), ' kg')
        print('     Ballonet mass: ', round(self.mass_ballonet, 2), ' kg')
        print('     Undercarriage mass: ', round(self.mass_undercarriage, 2), ' kg')
        print('     Propulsion mass: ', round(self.mass_propulsion, 2), ' kg')
        print('     Electronics mass: ', round(self.mass_electronics, 2), ' kg')
        print('     Payload mass: ', round(self.mass_payload, 2), ' kg')
        print()
        print('Balloon radius: ', round(self.radius, 2), ' m')
        print('Balloon length: ', round(self.length, 2), ' m')
        print('Balloon volume: ', round(self.volume, 2), ' m^3')
        print('Explosive potential: ', round(self.explosive_potential/1000000, 2), ' MJ')
        print('Spheroid ratio: ', round(self.spheroid_ratio, 0))
        print()
        print('Number of engines:', round(self.n_engines, 0))
        print('Generated power: ', round(self.power_solar/1000, 2), ' kW')
        print('Solar panel area: ', round(self.area_solar, 2), ' m^2')
        print()
        print('Drag coefficient: ', round(self.CD, 4))
        print('Cruise Speed: ', round(self.cruiseV, 3), ' m/s')

    def setCruiseSpeed(self, v_target, plot=False):
        print('designing Blimp for cruise speed of ', v_target, 'm/s')
        alphas = []
        vs = []
        vols = []
        masses = []
        radii = []
        self.panel_rows = -1
        while self.panel_angle < np.radians(170):
            print(np.degrees(self.panel_angle))
            self.panel_rows += 1
            for i in np.arange(0, 200, 1):
                self.mass_total = self.mass_payload + self.mass_undercarriage + self.mass_propulsion + self.mass_electronics + self.mass_balloon + self.mass_solar_cell + self.mass_ballonet
                self.volume = self.mass_total / lift_h2
                self.explosive_potential = self.volume * self.liftgas.spec_energy
                self.sizeBalloon()
                self.panel_angle = self.panel_rows * self.solar_cell.width / self.radius
                self.sizeSolar()
                self.mass_solar_cell = self.area_solar * self.solar_cell.density
                self.ref_area = self.volume**(2/3)
                self.cruiseV = (2 * self.power_solar * prop_eff * motor_eff * prop_limit / rho / self.ref_area / self.CD)**(1/3)

            if plot:
                alphas.append(self.panel_angle)
                vs.append(self.cruiseV)
                vols.append(self.volume)
                masses.append(self.mass_total)
                radii.append(self.radius)
            print('volume [m3]: ', self.volume)
            print('mass [kg]: ', self.mass_total)
            print('velocity [m/s]: ', self.cruiseV)


            if self.cruiseV >= v_target:
                print('Target speed of ', v_target, ' m/s was reached.')
                break
            if self.radius >= REQ_max_radius:
                print('MAXIMUM RADIUS REACHED')
                break
            if self.length >= REQ_max_length:
                print('MAXIMUM LENGTH REACHED')
                break
            if self.explosive_potential >= REQ_max_explosive:
                print('MAXIMUM EXPLOSIVE POTENTIAL REACHED')
                break

        if plot:
                plt.plot(np.arange(0, self.panel_rows+1, 1), vs)
                plt.plot(np.arange(0, self.panel_rows+1, 1), radii)
                plt.plot(np.arange(0, self.panel_rows+1, 1), vols)
                plt.plot(np.arange(0, self.panel_rows+1, 1), masses)
                plt.legend(['Velocity', 'Radius', 'Volume', 'Mass'])
                plt.grid()
                plt.xlabel('Number of solar panels per row')
                plt.show()

        self.n_panels = 2 * self.panel_rows * round(self.length_factor * self.length / self.solar_cell.width, 0)
        self.power_available = self.power_solar * motor_eff * prop_eff * prop_limit
        self.power_per_engine = self.power_available / self.n_engines


    def estimateCost(self):
        cost = self.n_panels
        return cost

########################### END OF CLASS DEF ############################### END OF CLASS DEF #######################################



#Blimp Initialisation
Shlimp = Blimp(mass_payload =       REQ_payload_mass,  # [kg]
               mass_undercarriage=   3,  # [kg]
               mass_propulsion=      0.8,  # [kg]
               mass_electronics=     1,  # [kg]
               n_engines=            2,
               mass_ballonet=        0.75,  # [kg]
               length_factor=        0.8,
               spheroid_ratio=       3,
               liftgas=             gas.hydrogen,
               solar_cell=          sc.maxeon_gen3)

Shlimp.setCruiseSpeed(minimum_velocity, plot=True)
Shlimp.report()
# plot_blimp(Shlimp)




