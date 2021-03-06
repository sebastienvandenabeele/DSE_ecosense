import numpy as np
import matplotlib.pyplot as plt
import solar_sizing as solar
import pickle as pick
import requirements as req
from Classes import electronics as el, engines as eng, materials as mat, gas, battery as bat
from control_surface import sizeControl
from drag_coefficient import calculateCD
import structures as struc
from simulator import *
from altitude_control import *

def pickle(obj, filename):
    with open('Pickle Shelf/' + filename, 'wb') as file:
        pick.dump(obj, file)

def unpickle(filename):
    with open('Pickle Shelf/' + filename, 'rb') as file:
        return pick.load(file)

###################
# Constants
###################

# Physical Constants
lift_he                         = 1.0465 #    kg lift per cubic meter
lift_h2                          = 1.14125
p                               = 1.6075  # []          Constant for ellipsoid calculation

# Propulsion constants
prop_eff                        = 0.7981 # Set by Louis design
prop_limit                      = 0.55

# Environment
avg_sun_elevation               = 52  # [deg]
rho                             = 1.225  # [kg/m3]


###################
# Requirement inputs
###################
margin                          = 1.2
iteration_precision = 0.001


# Creation of Blimp class
class Blimp:
    def __init__(self, name, mass_fire_ex=0, target_speed=0, mass_payload=0, envelope_material=0, liftgas=0,mass_gondola_structure=0, mass_deployment=0, gondola=0, x_l_fins=0.9, trip_time=7,
                  mass_ballonet=0, solar_cell=0, engine=0, gondola_electronics=[], envelope_electronics=[], length_factor=0, spheroid_ratio=0, n_engines=0, n_engines_rod=0,
                 mass_solar_cell=0, mass_balloon=0, panel_angle=0, mass_control=0, n_fins=0, h_trim=0, balloon_pressure=0, d_eng=0):
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
        self.n_engines_rod=n_engines_rod
        if self.n_engines_rod==1:
            self.mass_engine_mount=0.536487
        elif self.n_engines_rod==2:
            self.mass_engine_mount=0.36
        self.mass_servo=0.197
        self.mass_esc=0.109
        #self.mass['engines'] = (self.engine.mass+self.mass_esc) * self.n_engines + self.n_engines/self.n_engines_rod*(self.mass_engine_mount+self.mass_servo)   # margin for mounting, esc, servo
        self.mass['engines'] = (0.788 + self.engine.mass + self.mass_esc) * self.n_engines
        self.installed_engine_power = self.n_engines * self.engine.max_power * prop_limit
        self.x_eng = 0
        self.z_eng = -1
        self.d_eng = d_eng

        # Solar cells
        self.solar_cell = solar_cell
        self.panel_angle = panel_angle
        self.length_factor = length_factor
        self.area_solar = 0
        self.generated_power = 0

        # Balloon Aerodynamics
        self.h_trim = h_trim
        self.balloon_pressure = balloon_pressure
        self.lift_factor = setLiftConstant(h_trim, self.balloon_pressure)
        print('Lift factor: ', self.lift_factor)
        self.spheroid_ratio = spheroid_ratio
        self.CD = 0.02
        self.liftgas = liftgas
        self.n_fins = n_fins
        self.x_l_fins = x_l_fins
        self.h_trim = h_trim

        # Materials
        self.material = {'envelope': envelope_material}

        # Masses
        self.x_cg = 0
        self.z_cg = 0
        self.mass['payload'] = mass_payload
        self.mass['gondola structure'] = mass_gondola_structure
        self.mass['controls'] = mass_control
        self.gondola = gondola

        self.gondola_electronics = gondola_electronics
        self.envelope_electronics = envelope_electronics
        self.power_electronics = sum([el.constant_power_consumption for el in self.envelope_electronics]) + sum([el.constant_power_consumption for el in self.gondola_electronics])
        self.mass['envelope electronics'] = sum([el.mass for el in self.envelope_electronics])
        self.mass['gondola electronics'] = sum([el.mass for el in self.gondola_electronics])

        self.mass['solar'] = mass_solar_cell
        self.mass['envelope'] = mass_balloon
        self.mass['deployment'] = mass_deployment
        self.mass['ballonets'] = mass_ballonet
        self.mass['battery'] = 0
        self.mass['fire extinguising'] = mass_fire_ex

        self.MTOM = sum(self.mass.values())
        self.volume = self.MTOM / lift_h2
        self.n_engines = n_engines

        self.trip_time = trip_time
        self.target_speed = target_speed
        self.setCruiseSpeed(plot=False)
        self.MTOW = self.MTOM * g
        self.cruise_thrust = self.net_prop_power / self.cruiseV
        self.power_per_engine = self.gross_prop_power / self.n_engines
        self.cruise_throttle = self.power_per_engine / self.engine.max_power
        self.n_panels = self.area_solar * self.solar_cell.fillfac / self.solar_cell.area
        self.estimateCG()
        self.placeGondola()
        self.vol_ventedH2 = self.mass['payload'] / self.MTOM * self.volume
        self.range = self.cruiseV * self.trip_time   # m
        self.deployment_distance = self.range - 200000  # m
        self.deployment_time = self.deployment_distance / self.cruiseV   # s
        self.venting_vol_flow = self.vol_ventedH2 / self.deployment_time

    def save(self):
        pickle(self, self.name)

    def sizeBalloon(self):
        """
        lifting body estimation subroutine for iteration
        """
        self.volume = self.MTOM / self.lift_factor
        self.explosive_potential = self.volume * self.liftgas.spec_energy
        self.radius = ((3 * self.volume) / (4 * self.spheroid_ratio * np.pi)) ** (1 / 3)
        self.length = self.spheroid_ratio * self.radius * 2
        self.balloon_thickness = struc.envelope_thickness(self, struc.envelope_pressure(self))

        self.radius_ballonet = (self.mass['payload'] / self.MTOM * self.volume * 3 / 8 / np.pi)**(1/3)
        self.mass['ballonets'] = 2 * 4 * np.pi * self.radius_ballonet**2 * 0.0584
        #self.mass['ballonets'] = 11.2
        self.surface_area = 4*np.pi * ((self.radius**(2*p) + 2*(self.radius*self.length/2)**p)/3)**(1/p)
        self.mass['envelope'] = self.surface_area * 0.192
        self.ref_area = self.volume ** (2 / 3)

    def sizeBattery(self):
        dod = 0.9  # depth of discharge
        voltage_nominal = 3.7  # [V]
        n_series = 12

        self.battery_speed = (prop_eff * self.engine.efficiency * self.power_electronics / (rho * self.ref_area * self.CD)) ** (1 / 3)  # [m/s]
        self.battery_capacity = (1.5 * self.power_electronics * req.range_on_battery) / (self.battery_speed) * 1.1  + 600000# [J]
        self.battery_pack = bat.BatteryPack(self.battery_capacity, dod)
        self.mass['battery'] = self.battery_pack.mass
        self.battery_charge = self.battery_capacity / (n_series * voltage_nominal)  # [As]

    def report(self):
        """
        User-friendly output of most important design characteristics
        """
        print('###################### DESIGN CHARACTERISTICS ###################################')
        print()
        print('MTOM: ', round(self.MTOM, 2), ' kg')
        print('MTOW: ', round(self.MTOW, 2), ' N')
        for key, value in self.mass.items():
            print('Mass of', key, ':', round(value, 2), "kg")
        print()
        print('Balloon radius: ', round(self.radius, 2), ' m')
        print('Balloon length: ', round(self.length, 2), ' m')
        print('Balloon volume: ', round(self.volume, 2), ' m^3')
        print('Balloon thickness: ', round(self.balloon_thickness*1000, 3), ' mm')
        print('Balloon surface area: ', round(self.surface_area, 1), ' m^2')
        print('Explosive potential: ', round(self.explosive_potential/10**6, 2), ' MJ')
        print('Vented hydrogen per mission:', round(self.vol_ventedH2, 2), 'm^3')
        print('Maximum trim altitude at full loading: ', (round(self.h_trim, 2)), 'm SL')
        print('Spheroid ratio: ', round(self.spheroid_ratio, 0))
        print('Number of fins: ', self.n_fins)
        print()
        print('C.g. located at x: ' + str(round(self.x_cg, 2)) + ' m, z: ' + str(round(self.z_cg, 2)) + ' m')
        print('Gondola at x:', round(self.gondola.x_cg, 2), 'm, z: ', round(self.gondola.z_cg, 2), 'm')
        print('Engine assembly cg at x:', round(self.x_eng, 2), 'm, z:', round(self.z_eng, 2), 'm')
        print('Hangdown angle at take-off: ', round(np.arctan(self.x_cg / self.z_cg) * 57.3, 2), ' degrees')
        print()
        print('Number of solar panels: ', int(round(self.n_panels, 0)))
        print('Solar panel area: ', round(self.area_solar, 2), ' m^2')
        print('Solar panel coverage angle: ', round(self.panel_angle * 57.3, 0), ' degrees')
        print('Generated power: ', round(self.generated_power / 1000, 2), ' kW')
        print('On-board electronics power: ', int(round(self.power_electronics, 0)), ' W')
        print('Engines Electronics power: ', round(self.gross_prop_power/1000, 2), 'kW')
        print('Electronic Power per engine:', round(self.power_per_engine / 1000, 2), 'kW')
        print('Engine type: ', self.engine.name)
        print('Single engine max power: ', round(self.engine.max_power / 1000, 2), ' kW')
        print('Number of engines:', self.n_engines)
        print('Actual propulsion power available: ', round(self.net_prop_power / 1000, 2), ' kW')
        print('Cruise throttle ', round(self.cruise_throttle * 100, 1), ' % (out of 55% recommended for steady-state)')
        print('Cruise thrust: ', round(self.cruise_thrust, 2), ' N')
        print()
        print('Drag coefficient: ', round(self.CD, 4))
        print('Speed on battery: ', round(self.battery_speed * 3.6, 2), ' km/h')
        print('Return time on battery: ', round(req.range_on_battery/self.battery_speed/3600, 1), ' h')
        print('Cruise Speed: ', round(self.cruiseV * 3.6, 2), ' km/h')
        print('Range: ', round(self.range/1000, 2), ' km')
        print('Mission time', round(self.trip_time / 3600, 2), ' h')
        print('Deployment distance:', round(self.deployment_distance / 1000, 2), ' km')
        print('Deployment time:', round(self.deployment_time / 3600, 2), ' h')


    def trim(self, cruisepath):
        self.h_trim = np.mean(cruisepath)

    def setCruiseSpeed(self, plot=False):
        """
        :param v_target: target cruise speed, blimp should be sized for
        :param plot: boolean, if iteration results should be plotted

        performs design iterations for solar panel area and balloon volume to reach a given cruise speed
        """
        vs = [0]


        requirements_met = True
        print('Iteration initialised.')
        # One row of solar panels is added along the perimeter
        dalpha = self.solar_cell.width / 2
        while self.panel_angle < np.radians(350) and requirements_met:
            self.panel_angle += dalpha
            masses = []
            for i in np.arange(0, 50, 1):  # Iterative Calculations
                self.MTOM = sum(self.mass.values()) #- self.mass['payload']
                masses.append(self.MTOM)
                self.sizeBalloon()
                self.fin=sizeControl(self)
                self.mass["controls"]=self.fin.mass * self.n_fins
                self.sizeBattery()

                if i % 4 == 0:
                    self.area_solar, self.generated_power, self.mass['solar'] = solar.sizeSolar(self)  # Electrical Power generated by panels
                self.power_for_prop = (self.generated_power * 0.8 - self.power_electronics)                     # Electrical Power left for propulsion
                self.gross_prop_power = min(self.power_for_prop, self.installed_engine_power)          # Available electrical power for propulsion
                self.net_prop_power = self.gross_prop_power * self.engine.efficiency * prop_eff        # Converting available elerical power to propulsive power


                self.cruiseV = (2 * self.net_prop_power / rho / self.ref_area / self.CD) ** (1 / 3)
                if not np.isnan(calculateCD(self)):
                    self.CD = calculateCD(self) #+ 0.065 / self.ref_area
                if i > 2:
                    if np.abs(masses[-1] - masses[-2]) < iteration_precision:
                        print(i, ' iterations needed')
                        break
                #self.range = self.cruiseV * maximum_triptime
            print('Progress: ', round(self.cruiseV/self.target_speed * 100, 0), ' %')

            # Addition of solar panels is stopped if requirements are infringed
            requirements_met = req.checkRequirements(self)
            if self.cruiseV >= self.target_speed:
                print('Target design speed reached.')
                break
            if np.abs(self.power_for_prop - self.installed_engine_power) <= 10:
                print('Engine limit reached')
                break
            if self.cruiseV < vs[-1]:
                print('Could not reach target speed!')
                break
            vs.append(self.cruiseV)

        print('Iteration done.')

    def estimateCost(self):
        """
        adds and orders all costs from used parts
        """


        cost = {}
        cost['solar'] = self.n_panels * self.solar_cell.cost
        cost['hydrogen'] = self.volume * self.liftgas.cost
        cost['electronics'] = sum([device.cost for device in np.append(self.envelope_electronics, self.gondola_electronics)])
        cost['engines'] = self.n_engines * self.engine.cost * 1.2
        cost['envelope'] = self.mass['envelope'] * self.material['envelope'].cost
        cost['deployment'] = 1000
        cost['fins'] = self.n_fins * (100 + 30)
        #cost['battery'] = self.battery_pack.cost

        print()
        print('############ COST ESTIMATION ################')
        print('Total cost:', round(sum(cost.values()), 2), 'EUR')
        for key, value in cost.items():
            print('Cost of', key, ':', round(value, 2), 'EUR')

    def estimateCG(self):
        """
        Estimation of Blimp c.g. in the plane of symmetry. Datum is the centroid of the envelope. Positive z up, positive x along longitudinal.
        :return: x_bar: x-coordinate of c.g. [m]
        :return: z_bar: z-coordinate of c.g. [m]
        """

        x = {}
        z = {}
        mass = {}

        x['envelope'] = 0
        z['envelope'] = 0
        mass['envelope'] = self.mass['envelope']

        x['gondola'] = self.gondola.x_cg
        z['gondola'] = self.gondola.z_cg
        mass['gondola'] = self.mass['gondola structure'] + self.mass['gondola electronics'] + self.mass['payload'] + self.mass['battery'] + self.mass['deployment']

        x['engines'] = self.x_eng
        z['engines'] = self.z_eng
        mass['engines'] = self.mass['engines']

        x['controls'] = self.x_l_fins * self.length - self.length / 2
        z['controls'] = 0
        mass['controls'] = self.mass['controls']

        x['ballonets'] = 0
        z['ballonets'] = - self.radius + self.radius_ballonet
        mass['ballonets'] = self.mass['ballonets']

        x['solar'] = 0
        angle = self.panel_angle / 2
        if angle <= np.pi / 2:
            z['solar'] = self.radius * (angle + np.cos(angle) * np.sin(angle)/(2*np.sin(angle)) )
        else:
            print('Solar panel c.g. estimation incomplete!')
            z['solar'] = 0.5 * self.radius
            # TODO: implement accurate estimation for angles larger than 90 deg
        mass['solar'] = self.mass['solar']

        self.x_cg = sum([x[key] * mass[key] for key in x.keys()]) / sum(mass.values())
        self.z_cg = sum([z[key] * mass[key] for key in x.keys()]) / sum(mass.values())
        self.Iyy = sum([(x[key]**2 + z[key]**2) * mass[key] for key in x.keys()])
        self.Iyy += mass['engines'] * self.d_eng**2
        self.Iyy += mass['envelope'] * self.radius * self.length * 2/3

        print(self.Iyy)

    def placeGondola(self):
        self.gondola.z_cg = -2.1
        self.gondola.x_cg = 0
        self.z_eng = -1.968
        # for i in range(4):
        #     self.x_eng = self.x_cg
        #     self.estimateCG()
        xcg_target = self.cruise_thrust * self.z_eng / self.MTOW
        for x_gondola in np.arange(0, self.length / 4, 0.01):
            self.gondola.x_cg = -x_gondola
            self.x_eng = xcg_target


            self.estimateCG()
            if np.abs(xcg_target - self.x_cg) < 0.005:
                break



