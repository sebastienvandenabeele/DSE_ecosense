import numpy as np
import matplotlib.pyplot as plt
from projected_panel import plot_blimp, irradiance_distribution
from Classes import solarcells as sc, gas
import pickle as pick
import requirements as req
from Classes import electronics as el, engines as eng, materials as mat
from control_surface import sizeControl
from drag_coefficient import calculateCD
import structures2 as struc
from simulator import *

def pickle(obj, filename):
    with open('Pickle Shelf/' + filename, 'wb') as file:
        pick.dump(obj, file)

def unpickle(filename):
    with open('Pickle Shelf/' + filename, 'rb') as file:
        return pick.load(file)

###################
# Constants
###################

#Physical Constants
lift_he                         = 1.0465 #    kg lift per cubic meter
lift_h2                          = 1.14125
p                               = 1.6075  # []          Constant for ellipsoid calculation

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
fin_foam_density                = 15 # [kg/m3]
fin_wood_density                = 150 # [kg/m3]

prop_eff                        = 0.8
motor_eff                       = 0.9
prop_limit                      = 0.55

#Environment
avg_sun_elevation               = 52  # [deg]
#tmy = read_irradiance()
tmy = unpickle('tmy.txt')
rho                             = 1.225  # [kg/m3]




###################
# Requirement inputs
###################
margin                          = 1.2
maximum_triptime                = 5 * 3600  # [s]
minimum_velocity                = req.range / maximum_triptime

REQ_n_sensors                   = 1295 / 2
relays_per_sensor               = 25
n_relays                        = int(round(REQ_n_sensors / relays_per_sensor, 0))
m_sensor                        = 0.052      # [kg]
m_relay                         = 0.338     # [kg]
m_deployment_system             = 2         # [kg]
REQ_payload_mass                = n_relays * m_relay + REQ_n_sensors * m_sensor + m_deployment_system



# Creation of Blimp class
class Blimp:
    def __init__(self, name, target_speed=0, mass_payload=0, mass_gondola=0, envelope_material=0, liftgas=0, mass_deployment=0,
                 mass_electronics=0, mass_ballonet=0, solar_cell=0, engine=0, electronics=[], length_factor=0, spheroid_ratio=0, n_engines=0,
                 mass_solar_cell=0, mass_balloon=0, panel_angle=0, mass_control=0, n_controls=0):
        """
        A class describing a virtual blimp object, used as vehicle design model
        :param name: [str] Name of instance
        :param mass_payload: [float] Design payload mass [kg]
        :param mass_gondola: [float] Mass estimate of gondola [kg]
        :param mass_propulsion: [float] Mass estimate of propulsion system [kg]
        :param liftgas: [gas] gas used for lifting
        :param mass_deployment: [float] Mass estimate of deployment system [kg]
        :param mass_electronics: [float] Mass estimate of on-board electronics [kg]
        :param mass_ballonet: [float] Mass estimate of ballonets [kg]
        :param solar_cell: [solarcell] Solar cell model used
        :param length_factor: [float] Percentage of length covered in solar cells (0.0 - 1.0)
        :param spheroid_ratio: [float] Mathematical parameter for balloon calculations [-]
        :param n_engines: [int] number of engines [-]
        :param mass_solar_cell: [float] Mass estimate of solar cells [kg]
        :param mass_balloon: [float] Mass estimate of balloon envelope [kg]
        :param panel_angle: [float] One-sided angle from the top of the balloon, describing how much of the surface
                is covered in solar cells [rad]
        """
        self.name = name
        self.mass = {}
        # Propulsion
        self.n_engines = n_engines
        self.engine = engine
        self.mass['engines'] = self.engine.mass * n_engines * 1.5 # margin for mounting and prop
        self.cruise_prop_power = self.n_engines * self.engine.max_power * self.engine.efficiency * prop_limit * prop_eff
        print("Power deliverable by the engines: ", self.cruise_prop_power)

        # Solar cells
        self.solar_cell = solar_cell
        self.panel_angle = panel_angle
        self.length_factor = length_factor
        self.panel_rows = -1
        self.area_solar = 0
        self.power_solar = 0


        # Balloon Aerodynamics
        self.spheroid_ratio = spheroid_ratio
        dl = 1 / spheroid_ratio
        ld = spheroid_ratio
        list_element = min(dl_re[:, 0], key=lambda x: abs(x - dl))
        re = dl_re[np.where(dl_re[:, 0] == list_element), 1][0][0]
        self.CD = (0.172 * ld ** (1 / 3) + 0.252 * dl ** 1.2 + 1.032 * dl ** 2.7) / ((re * 10 ** 7) ** (1 / 6)) * margin
        self.liftgas = liftgas
        self.n_controls = n_controls


        # Materials
        self.material = {'envelope': envelope_material}

        # Masses

        self.mass['payload'] = mass_payload
        self.mass['gondola'] = 0.15 * mass_payload
        self.mass['control'] = mass_control

        self.electronics = electronics
        self.power_electronics = sum([el.power_consumption for el in self.electronics])
        self.mass['electronics'] = sum([el.mass for el in self.electronics])

        self.mass['solar'] = mass_solar_cell
        self.mass['envelope'] = mass_balloon
        self.mass['deployment'] = mass_deployment
        self.mass['ballonet'] = mass_ballonet
        self.mass['battery'] = 0

        self.MTOM = sum(self.mass.values())
        self.volume = self.MTOM / lift_h2
        self.n_engines = n_engines

        self.target_speed = target_speed
        self.setCruiseSpeed(plot=False)

    def save(self):
        pickle(self, self.name)

    def sizeSolar(self):
        """
        solar power estimation subroutine for iteration
        """
        self.panel_angle = self.panel_rows * self.solar_cell.width / self.radius
        self.area_solar = 0.8 * 2 * self.length / 2 * self.radius * 2 * self.panel_angle

        shone_area = self.area_solar * irradiance_distribution(self, avg_sun_elevation)
        net_power = shone_area * np.mean(tmy["DNI"]) + np.mean(tmy["DHI"]) * self.area_solar
        self.power_solar = net_power * self.solar_cell.efficiency * self.solar_cell.fillfac
        self.mass['solar'] = self.area_solar * self.solar_cell.density

        if np.isnan(self.power_solar):
            self.power_solar = 0

    def sizeBalloon(self):
        """
        lifting body estimation subroutine for iteration
        """
        self.volume = self.MTOM / lift_h2
        self.explosive_potential = self.volume * self.liftgas.spec_energy
        self.radius = ((3 * self.volume) / (4 * self.spheroid_ratio)) ** (1 / 3)
        self.length = self.spheroid_ratio * self.radius * 2
        self.balloon_thickness = struc.envelope_thickness(self, struc.envelope_pressure(self))
        self.surface_area = 4*np.pi * ((self.radius**(2*p) + 2*(self.radius*self.length/2)**p)/3)**(1/p)
        self.mass['envelope'] = self.surface_area * self.balloon_thickness * self.material['envelope'].density
        self.ref_area = self.volume ** (2 / 3)
        
    def sizeBattery(self):
        dod=0.9 
        battery_density = 250 # [Wh/kg]
        voltage_nominal=3.7 # [V]
        n_series=12
        

        self.battery_speed = (2 * prop_eff * motor_eff * self.power_electronics / (rho * self.ref_area * self.CD)) ** (
                    1 / 3)
        self.battery_capacity= 2 * self.power_electronics * req.range_on_battery / 1000 / (self.battery_speed * 3.6) / dod * margin
        self.mass['battery'] = self.battery_capacity / battery_density
        self.battery_capacity= self.battery_capacity / (n_series * voltage_nominal)

    def report(self):
        """
        User-friendly output of most important design characteristics
        """
        print('###################### DESIGN CHARACTERISTICS ###################################')
        print()
        print('Number of sensors: ', round(REQ_n_sensors, 0))
        print('Number of relays: ', n_relays)
        print()
        print('MTOM: ', round(self.MTOM, 2), ' kg')
        for key, value in self.mass.items():
            print('Mass of', key, ':', round(value, 2), "kg")
        print()
        print('Balloon radius: ', round(self.radius, 2), ' m')
        print('Balloon length: ', round(self.length, 2), ' m')
        print('Balloon volume: ', round(self.volume, 2), ' m^3')
        print('Balloon thickness: ', round(self.balloon_thickness*1000, 3), ' mm')
        print('Balloon surface area: ', round(self.surface_area, 1), ' m^2')
        print('Explosive potential: ', round(self.explosive_potential/1000000, 2), ' MJ')
        print('Spheroid ratio: ', round(self.spheroid_ratio, 0))
        print('Number of control surfaces: ', self.n_controls)
        print()
        print('Number of solar panels: ', round(self.n_panels, 0))
        print('Solar panel area: ', round(self.area_solar, 2), ' m^2')
        print('Generated power: ', round(self.power_solar/1000, 2), ' kW')
        print('On-board electronics power: ', round(self.power_electronics, 2), ' W')
        print()
        print('Engine type: ', self.engine.name)
        print('Single engine max power: ', round(self.engine.max_power / 1000, 2), ' kW')
        print('Number of engines:', round(self.n_engines, 0))
        print('Actual propulsion power available: ', round(self.prop_power_available / 1000, 2), ' kW')
        print('Actual power delivered per engine: ', round(self.power_per_engine/1000, 2), ' kW')
        print('Engine utilization ', round(self.power_per_engine / self.engine.max_power / self.engine.efficiency / prop_eff * 100, 1), ' % (out of 55% steady-state)')
        print()
        print('Drag coefficient: ', round(self.CD, 4))
        print('Battery Speed: ', round(self.battery_speed * 3.6, 2), ' km/h')
        print('Return time on battery: ', round(req.range_on_battery/self.battery_speed/3600, 1), ' h')
        print('Cruise Speed: ', round(self.cruiseV*3.6, 2), ' km/h')
        print('Range on 1 day: ', round(self.range/1000, 1), ' km')

    def setCruiseSpeed(self, plot=False):
        """
        :param v_target: target cruise speed, blimp should be sized for
        :param plot: boolean, if iteration results should be plotted

        performs design iterations for solar panel area and balloon volume to reach a given cruise speed
        """

        alphas = []
        vs = []
        vols = []
        masses = []
        radii = []

        requirements_met = True
        print('Iteration initialised.')
        # One row of solar panels is added along the perimeter
        while self.panel_angle < np.radians(178) and requirements_met:
            self.panel_rows += 1
            for i in np.arange(0, 50, 1):  # Iterative Calculations
                self.MTOM = sum(self.mass.values())
                self.sizeBalloon()
                self.sizeSolar()
                self.sizeBattery()
                self.mass['control'], self.control_surface, self.control_chord=sizeControl(self)
                # self.mass['control'] = sizeControl(self)*(0.95*fin_foam_density+0.05*fin_wood_density)

                # Uncomment this if an engine is selected
                self.solar_power_available = (self.power_solar - self.power_electronics) * self.engine.efficiency * prop_eff
                self.prop_power_available = min([self.cruise_prop_power, self.solar_power_available])


                # Uncomment this if no engine is selected
                # self.prop_power_available = self.power_solar * motor_eff * prop_eff
                # self.mass_propulsion = eng.weight_per_W * self.power_solar
                # if np.isnan(self.mass_propulsion):
                #     self.mass_propulsion = 0


                self.cruiseV = (2 * self.prop_power_available / rho / self.ref_area / self.CD) ** (1 / 3)
                if not np.isnan(calculateCD(self, rho)): 
                    self.CD = calculateCD(self, rho)
                self.range = self.cruiseV * maximum_triptime
            print('Progress: ', round(self.cruiseV/self.target_speed * 100, 0), ' %')
            if plot:
                alphas.append(self.panel_angle)
                vs.append(self.cruiseV)
                vols.append(self.volume)
                masses.append(self.MTOM)
                radii.append(self.radius)

            # Addition of solar panels is stopped if requirements are infringed
            requirements_met = req.checkRequirements(self)
            if self.cruiseV >= self.target_speed:
                print('Target design speed reached.')
                break
            if np.abs(self.prop_power_available - self.cruise_prop_power) <= 10:
                print('Engine limit reached')
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
        print('Iteration done.')
        self.n_panels = 2 * self.panel_rows * round(self.length_factor * self.length / self.solar_cell.width, 0)
        self.power_per_engine = self.prop_power_available / self.n_engines

    def estimateCost(self):
        """
        adds and orders all costs from used parts
        """


        cost = {}
        cost['solar'] = self.n_panels * self.solar_cell.cost
        cost['hydrogen'] = self.volume * self.liftgas.cost
        cost['electronics'] = sum([device.cost for device in self.electronics])
        cost['engines'] = self.n_engines * self.engine.cost * 1.2
        #cost['envelope'] = self.surface_area * self.material['envelope'].cost
        cost['deployment'] = 1000

        print()
        print('############ COST ESTIMATION ################')
        print('Total cost:', round(sum(cost.values()), 2), 'EUR')
        for key, value in cost.items():
            print('Cost of', key, ':', round(value, 2), 'EUR')





########################### END OF CLASS DEFINITION ############################### END OF CLASS DEFINTION #######################################



# Creation of blimp design, run either this or unpickle from file
Shlimp = Blimp(name=                "Shlimp_350km_2405_1603",
               mass_payload =       REQ_payload_mass,
               target_speed=        minimum_velocity,
               mass_deployment=      1,
               n_controls=           3,

               envelope_material=mat.polyethylene_fiber,

               n_engines=            4,
               engine=              eng.tmt_4130_300,

               electronics=         el.config_first_order,
               mass_ballonet=        8,
               length_factor=        0.8,
               spheroid_ratio=       3,
               liftgas=             gas.hydrogen,
               solar_cell=          sc.maxeon_gen3)
#
Shlimp.save()
#Shlimp = unpickle('Shlimp_350km_2405_1208')
Shlimp.report()
#calculateAltitudeGain(Shlimp)
Shlimp.estimateCost()
#simulateCruiseAcceleration(Shlimp)
#simulateVelocity(Shlimp, v0=Shlimp.cruiseV, throttle=0, tmax=50)
#Shlimp.report()
#plot_blimp(Shlimp)






