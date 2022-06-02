import numpy as np
import matplotlib.pyplot as plt
import solar_sizing as solar
import pickle as pick
import requirements as req
from Classes import electronics as el, engines as eng, materials as mat, gas
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

#Physical Constants
lift_he                         = 1.0465 #    kg lift per cubic meter
lift_h2                          = 1.14125
p                               = 1.6075  # []          Constant for ellipsoid calculation

prop_eff                        = 0.8065 # Set by Louis design
prop_limit                      = 0.55

#Environment
avg_sun_elevation               = 52  # [deg]


rho                             = 1.225  # [kg/m3]


###################
# Requirement inputs
###################
margin                          = 1.2

iteration_precision = 0.001


# Creation of Blimp class
class Blimp:
    def __init__(self, name, target_speed=0, mass_payload=0, mass_gondola=0, envelope_material=0, liftgas=0, mass_deployment=0,
                 mass_electronics=0, mass_ballonet=0, solar_cell=0, engine=0, electronics=[], length_factor=0, spheroid_ratio=0, n_engines=0,
                 mass_solar_cell=0, mass_balloon=0, panel_angle=0, mass_control=0, n_fins=0, h_trim=0, balloon_pressure=0):
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
        self.mass['engines'] = self.engine.mass * self.n_engines * 1.5  # margin for mounting
        self.mass['propellers'] = self.n_engines * 0.18  # Louis estimate
        self.cruise_prop_power = self.n_engines * self.engine.max_power * self.engine.efficiency * prop_limit * prop_eff

        # Solar cells
        self.solar_cell = solar_cell
        self.panel_angle = panel_angle
        self.length_factor = length_factor
        self.area_solar = 0
        self.power_solar = 0


        # Balloon Aerodynamics
        self.h_trim = h_trim
        self.balloon_pressure = balloon_pressure
        self.lift_factor = setLiftConstant(0, self.balloon_pressure)
        print('Lift factor: ', self.lift_factor)
        self.spheroid_ratio = spheroid_ratio
        self.CD = 0.02
        self.liftgas = liftgas
        self.n_fins = n_fins
        self.h_trim = h_trim


        # Materials
        self.material = {'envelope': envelope_material}

        # Masses
        self.x_bar = 0
        self.z_bar = 0
        self.mass['payload'] = mass_payload
        self.mass['gondola structure'] = 8
        self.mass['controls'] = mass_control

        self.electronics = electronics
        self.power_electronics = sum([el.power_consumption for el in self.electronics])
        self.mass['electronics'] = sum([el.mass for el in self.electronics])

        self.mass['solar'] = mass_solar_cell
        self.mass['envelope'] = mass_balloon
        self.mass['deployment'] = mass_deployment
        self.mass['ballonets'] = mass_ballonet
        self.mass['battery'] = 0

        self.MTOM = sum(self.mass.values())
        self.volume = self.MTOM / lift_h2
        self.n_engines = n_engines

        self.target_speed = target_speed
        self.setCruiseSpeed(plot=False)
        self.power_per_engine = self.prop_power_available / self.n_engines
        self.n_panels = self.area_solar * self.solar_cell.fillfac / self.solar_cell.area
        self.estimateCG()

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
        #self.mass['ballonets'] = 2 * 4 * np.pi * self.radius_ballonet**2 * 0.0584 + 1
        self.mass['ballonets'] = 11.2
        self.surface_area = 4*np.pi * ((self.radius**(2*p) + 2*(self.radius*self.length/2)**p)/3)**(1/p)
        self.mass['envelope'] = self.surface_area * 0.192
        self.ref_area = self.volume ** (2 / 3)

        
    def sizeBattery(self):
        dod = 0.9
        battery_density = 250 * 3600  # [J/kg]
        voltage_nominal = 3.7  # [V]
        n_series = 12

        self.battery_speed = (prop_eff * self.engine.efficiency * self.power_electronics / (rho * self.ref_area * self.CD)) ** (1 / 3) # [m/s]
        self.battery_capacity= (1.5 * self.power_electronics * req.range_on_battery) / (self.battery_speed * dod) * 1.1     # [J]
        self.mass['battery'] = self.battery_capacity / battery_density
        self.battery_charge= self.battery_capacity / (n_series * voltage_nominal)

    def report(self):
        """
        User-friendly output of most important design characteristics
        """
        print('###################### DESIGN CHARACTERISTICS ###################################')
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
        print('Explosive potential: ', round(self.explosive_potential/10**6, 2), ' MJ')
        print('Spheroid ratio: ', round(self.spheroid_ratio, 0))
        print('Number of fins: ', self.n_fins)
        print('C.g. located at x: ' + str(round(self.x_bar / self.length * 100, 2)) + ' % length, z: ' + str(round(self.z_bar, 2)) + ' m')
        print()
        print('Number of solar panels: ', int(round(self.n_panels, 0)))
        print('Solar panel area: ', round(self.area_solar, 2), ' m^2')
        print('Solar panel coverage angle: ', round(self.panel_angle * 57.3, 0), ' degrees')
        print('Generated power: ', round(self.power_solar/1000, 2), ' kW')
        print('On-board electronics power: ', int(round(self.power_electronics, 0)), ' W')
        print()
        print('Engine type: ', self.engine.name)
        print('Single engine max power: ', round(self.engine.max_power / 1000, 2), ' kW')
        print('Number of engines:', self.n_engines)
        print('Actual propulsion power available: ', round(self.prop_power_available / 1000, 2), ' kW')
        print('Actual power delivered per engine: ', round(self.power_per_engine/1000, 2), ' kW')
        print('Cruise throttle ', round(self.power_per_engine / self.engine.max_power / self.engine.efficiency / prop_eff * 100, 1), ' % (out of 55% recommended for steady-state)')
        print()
        print('Drag coefficient: ', round(self.CD, 4))
        print('Speed on battery: ', round(self.battery_speed * 3.6, 2), ' km/h')
        print('Return time on battery: ', round(req.range_on_battery/self.battery_speed/3600, 1), ' h')
        print('Cruise Speed: ', round(self.cruiseV * 3.6, 2), ' km/h')

    def trim(self, cruisepath):
        self.h_trim = np.mean(cruisepath)


    def setCruiseSpeed(self, plot=False):
        """
        :param v_target: target cruise speed, blimp should be sized for
        :param plot: boolean, if iteration results should be plotted

        performs design iterations for solar panel area and balloon volume to reach a given cruise speed
        """

        alphas = []
        vs = [0]
        vols = []
        masses = []
        radii = []

        requirements_met = True
        print('Iteration initialised.')
        # One row of solar panels is added along the perimeter
        dalpha = self.solar_cell.width / 2
        while self.panel_angle < np.radians(350) and requirements_met:
            self.panel_angle += dalpha
            masses = []
            for i in np.arange(0, 50, 1):  # Iterative Calculations
                self.MTOM = sum(self.mass.values()) - self.mass['payload']
                masses.append(self.MTOM)
                self.sizeBalloon()
                if i % 4 == 0:
                    self.area_solar, self.power_solar, self.mass['solar'] = solar.sizeSolar(self)

                self.sizeBattery()
                self.mass['controls'], self.control_surface, self.control_chord = sizeControl(self)
                self.mass['gondola structure'] = 0.15 * (self.mass['payload'] + self.mass['electronics'] + self.mass['battery'])
                self.solar_power_available = (self.power_solar - self.power_electronics) * self.engine.efficiency * prop_eff
                self.prop_power_available = min([self.cruise_prop_power, self.solar_power_available])


                self.cruiseV = (2 * self.prop_power_available / rho / self.ref_area / self.CD) ** (1 / 3)
                if not np.isnan(calculateCD(self, rho)): 
                    self.CD = calculateCD(self, rho) + 0.065 / self.ref_area
                if i > 2:
                    if np.abs(masses[-1] - masses[-2]) < iteration_precision:
                        print(i, ' iterations needed')
                        break
                #self.range = self.cruiseV * maximum_triptime
            print('Progress: ', round(self.cruiseV/self.target_speed * 100, 0), ' %')

            if plot:
                alphas.append(self.panel_angle)
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
            # if self.cruiseV < vs[-1]:
            #     print('Could not reach target speed!')
            #     break
            vs.append(self.cruiseV)

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


    def estimateCost(self):
        """
        adds and orders all costs from used parts
        """


        cost = {}
        cost['solar'] = self.n_panels * self.solar_cell.cost
        cost['hydrogen'] = self.volume * self.liftgas.cost
        cost['electronics'] = sum([device.cost for device in self.electronics])
        cost['engines'] = self.n_engines * self.engine.cost * 1.2
        cost['envelope'] = self.mass['envelope'] * self.material['envelope'].cost
        cost['deployment'] = 1000
        cost['fins'] = self.n_fins * (100 + 30)

        print()
        print('############ COST ESTIMATION ################')
        print('Total cost:', round(sum(cost.values()), 2), 'EUR')
        for key, value in cost.items():
            print('Cost of', key, ':', round(value, 2), 'EUR')

    def estimateCG(self):
        """
        Estimation of Blimp c.g. in the plane of symmetry. Datum is the front tip of the envelope. Positive z up, positive x along longitudinal.
        :return: x_bar: x-coordinate of c.g. [m]
        :return: z_bar: z-coordinate of c.g. [m]
        """

        x = {}
        z = {}
        mass = {}

        x['balloon'] = self.length / 2
        z['balloon'] = 0
        mass['balloon'] = self.mass['envelope']

        x['gondola'] = self.length / 2
        z['gondola'] = -self.radius - 0.5
        mass['gondola'] = self.mass['gondola structure'] + self.mass['electronics'] + self.mass['payload'] + self.mass['engines'] + self.mass['battery'] + self.mass['deployment']

        x['controls'] = 0.9 * self.length
        z['controls'] = 0
        mass['controls'] = self.mass['controls']

        x['ballonets'] = self.length / 2
        z['ballonets'] = - self.radius + self.radius_ballonet
        mass['ballonets'] = self.mass['ballonets']

        x['solar'] = self.length / 2
        angle = self.panel_angle / 2
        if angle <= np.pi / 2:
            z['solar'] = self.radius * (angle + np.cos(angle) * np.sin(angle)/(2*np.sin(angle)) )
        else:
            print('Solar panel c.g. estimation incomplete!')
            z['solar'] = 0.5 * self.radius
            # TODO: implement accurate estimation for angles larger than 90 deg
        mass['solar'] = self.mass['solar']

        self.x_bar = sum([x[key] * mass[key] for key in x.keys()]) / sum(mass.values())
        self.z_bar = sum([z[key] * mass[key] for key in x.keys()]) / sum(mass.values())

        print('C.g. estimated for ', round(sum(mass.values()) / self.MTOM * 100, 1), ' % of the mass.')




