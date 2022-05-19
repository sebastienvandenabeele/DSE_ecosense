import numpy as np
import matplotlib.pyplot as plt
from projected_panel import plot_blimp, irradiance_distribution
from Classes import solarcells as sc, gas
import pickle as pick
import requirements as REQ

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
lift_he                         = 1.0465
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

prop_eff                        = 0.8
motor_eff                       = 0.9
prop_limit                      = 0.75

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
REQ_range                       = 300 * 1000    # [m]
minimum_velocity                = REQ_range / maximum_triptime

REQ_n_sensors                   = 1295 / 2
relays_per_sensor               = 25
n_relays                        = int(round(REQ_n_sensors / relays_per_sensor, 0))
m_sensor                        = 0.05      # [kg]
m_relay                         = 0.338     # [kg]
m_deployment_system             = 2         # [kg]
REQ_payload_mass                = n_relays * m_relay + REQ_n_sensors * m_sensor + m_deployment_system

REQ_max_radius                  = 40        # [m]
REQ_max_length                  = 200       # [m]
REQ_max_explosive               = 100000 * 10001000     # [J] TBD



# Creation of Blimp class
class Blimp:
    def __init__(self, name, mass_payload=0, mass_gondola=0, mass_propulsion=0, liftgas=0, mass_deployment=0,
                 mass_electronics=0, mass_ballonet=0, solar_cell=0, engine=0, length_factor=0, spheroid_ratio=0, n_engines=0,
                 mass_solar_cell=0, mass_balloon=0, panel_angle=0):
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

        # Solar cells
        self.solar_cell = solar_cell
        self.panel_angle = panel_angle
        self.length_factor = length_factor


        # Balloon Aerodynamics
        self.spheroid_ratio = spheroid_ratio
        dl = 1 / spheroid_ratio
        ld = spheroid_ratio
        list_element = min(dl_re[:, 0], key=lambda x: abs(x - dl))
        re = dl_re[np.where(dl_re[:, 0] == list_element), 1][0][0]
        self.CD = (0.172 * ld ** (1 / 3) + 0.252 * dl ** 1.2 + 1.032 * dl ** 2.7) / ((re * 10 ** 7) ** (1 / 6)) * margin
        self.liftgas = liftgas


        # Masses
        self.mass_payload = mass_payload
        self.mass_undercarriage = mass_gondola
        self.mass_propulsion = mass_propulsion
        self.mass_electronics = mass_electronics
        self.mass_balloon = mass_balloon
        self.mass_solar_cell = mass_solar_cell
        self.mass_ballonet = mass_ballonet
        self.mass_deployment = mass_deployment
        self.mass_total = mass_payload + mass_gondola + mass_propulsion + mass_electronics + mass_balloon + mass_solar_cell + mass_ballonet

        self.volume = self.mass_total/lift_h2
        self.n_engines = n_engines


    def sizeSolar(self):
        """
        solar power estimation subroutine for iteration
        """
        self.area_solar = 0.8 * 2 * self.length / 2 * self.radius * 2 * self.panel_angle
        minimum_area = 2 * np.sin(self.panel_angle) * self.radius * self.length_factor * 2 * self.length / 2 * np.cos(avg_sun_elevation)
        # maximum_area = (1 - np.cos(avg_sun_elevation + self.panel_angle)) * self.radius * 0.8 * 2 * self.length / 2
        minimum_area=self.area_solar*irradiance_distribution(self, avg_sun_elevation)
        # print(irradiance_distribution(self,avg_sun_elevation))
        power_max = minimum_area * np.mean(tmy["DNI"]) + np.mean(tmy["DHI"]) * self.area_solar
        self.power_solar = power_max * self.solar_cell.efficiency * self.solar_cell.fillfac

    def sizeBalloon(self):
        """
        lifting body estimation subroutine for iteration
        """
        self.radius = ((3 * self.volume) / (4 * self.spheroid_ratio)) ** (1 / 3)
        self.length = self.spheroid_ratio * self.radius * 2
        self.surface_area = 4*np.pi * ((self.radius**(2*p) + 2*(self.radius*self.length/2)**p)/3)**(1/p)
        self.mass_balloon = self.surface_area * (silk_density + foil_density)

    def report(self):
        """
        User-friendly output of most important design characteristics
        """
        print('###################### DESIGN CHARACTERISTICS ###################################')
        print()
        print('Number of sensors: ', round(REQ_n_sensors, 0))
        print('Number of relays: ', n_relays)
        print()
        print('MTOM: ', round(self.mass_total, 3), ' kg')
        print('     Solar panel mass: ', round(self.mass_solar_cell, 2), ' kg')
        print('     Balloon mass: ', round(self.mass_balloon, 2), ' kg')
        print('     Ballonet mass: ', round(self.mass_ballonet, 2), ' kg')
        print('     Undercarriage mass: ', round(self.mass_undercarriage, 2), ' kg')
        print('     Propulsion mass: ', round(self.mass_propulsion, 2), ' kg')
        print('     Electronics mass: ', round(self.mass_electronics, 2), ' kg')
        print('     Payload mass: ', round(self.mass_payload, 2), ' kg')
        print()
        print('Balloon radius: ', round(self.radius, 2), ' m')
        print('Balloon length: ', round(self.length, 2), ' m')
        print('Balloon volume: ', round(self.volume, 2), ' m^3')
        print('Balloon surface area: ', round(self.surface_area, 1), ' m^2')
        print('Explosive potential: ', round(self.explosive_potential/1000000, 2), ' MJ')
        print('Spheroid ratio: ', round(self.spheroid_ratio, 0))
        print()
        print('Number of solar panels: ', round(self.n_panels, 0))
        print('Solar panel area: ', round(self.area_solar, 2), ' m^2')
        print('Generated power: ', round(self.power_solar/1000, 2), ' kW')
        print('Power available: ', round(self.power_available/1000, 2), ' kW')
        print('Number of engines:', round(self.n_engines, 0))
        print('Power per engine: ', round(self.power_per_engine/1000, 2), ' kW')
        print()
        print('Drag coefficient: ', round(self.CD, 4))
        print('Cruise Speed: ', round(self.cruiseV, 2), ' m/s')
        print('Range on 1 day: ', round(self.range/1000, 1), ' km')

    def setCruiseSpeed(self, v_target, plot=False):
        """
        :param v_target: target cruise speed, blimp should be sized for
        :param plot: boolean, if iteration results should be plotted

        performs design iterations for solar panel area and balloon volume to reach a given cruise speed
        """

        print('designing Blimp for cruise speed of ', v_target, 'm/s')
        alphas = []
        vs = []
        vols = []
        masses = []
        radii = []
        self.panel_rows = -1
        # One row of solar panels is added along the perimeter
        while self.panel_angle < np.radians(178):
            print(np.degrees(self.panel_angle))
            self.panel_rows += 1
            for i in np.arange(0, 200, 1): # Iterative Calculations
                self.mass_total = self.mass_payload + self.mass_undercarriage + self.mass_propulsion + self.mass_electronics + self.mass_balloon + self.mass_solar_cell + self.mass_ballonet
                self.volume = self.mass_total / lift_h2
                self.explosive_potential = self.volume * self.liftgas.spec_energy
                self.sizeBalloon()
                self.panel_angle = self.panel_rows * self.solar_cell.width / self.radius
                self.sizeSolar()
                self.mass_solar_cell = self.area_solar * self.solar_cell.density
                self.ref_area = self.volume**(2/3)
                self.power_available = self.power_solar * motor_eff * prop_eff * prop_limit
                self.cruiseV = (2 * self.power_available / rho / self.ref_area / self.CD)**(1/3)
                self.range = self.cruiseV * maximum_triptime

            if plot:
                alphas.append(self.panel_angle)
                vs.append(self.cruiseV)
                vols.append(self.volume)
                masses.append(self.mass_total)
                radii.append(self.radius)
            print('volume [m3]: ', self.volume)
            print('mass [kg]: ', self.mass_total)
            print('velocity [m/s]: ', self.cruiseV)

            # Addition of solar panels is stopped if requirements are infringed
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
        self.power_per_engine = self.power_available / self.n_engines

    def estimateCost(self):
        """
        adds and orders all costs from used parts
        :return:
        """
        # TODO: basically everything, work in progress

        cost = {}
        cost['solar'] = self.n_panels * self.solar_cell.cost
        cost['h2'] = self.volume * self.liftgas.cost

        print(cost)

    def save(self):
        pickle(self, self.name)

########################### END OF CLASS DEFINITION ############################### END OF CLASS DEFINTION #######################################


def simulateVelocity(blimp, v0=0, throttle=1, tmax=30):
    """
    :param blimp: Instance of blimp class used for acceleration simulation
    :param v0: Initial velocity of blimp
    :param throttle: Throttle factor multiplied with steady-state power available
    :param tmax: simulation time
    """

    vs = [v0]
    ts = [0]
    v = 0
    E = 0.5 * v0**2 * blimp.mass_total
    dt = 0.1
    for t in np.arange(0, tmax, dt):
        v = np.sqrt(2 * E / blimp.mass_total)
        dP = blimp.power_available * throttle - 0.5 * rho * v**3 * blimp.ref_area * blimp.CD
        E += dP * dt

        ts.append(t)
        vs.append(v)

    plt.plot(ts, vs)
    plt.plot(ts, minimum_velocity * np.ones(len(ts)), linestyle='dashed', color='black')
    plt.grid()
    plt.xlim(0, tmax)
    plt.ylim(0, 18)
    plt.legend(['Current velocity', 'Design velocity'])
    plt.xlabel('Time [s]')
    plt.ylabel('Velocity [m/s]')
    #plt.savefig('acceleration.png')
    plt.show()




# Creation of blimp design, run either this or unpickle from file
# Shlimp = Blimp(name=                "Shlimp",
#                mass_payload =       REQ_payload_mass,  # [kg]
#                mass_undercarriage=   3,  # [kg]
#                mass_deployment=      1,  # [kg]
#                mass_propulsion=      2,  # [kg]
#                mass_electronics=     1,  # [kg]
#                n_engines=            2,
#                mass_ballonet=        0.75,  # [kg]
#                length_factor=        0.8,
#                spheroid_ratio=       3,
#                liftgas=             gas.hydrogen,
#                solar_cell=          sc.maxeon_gen3)

#Shlimp.setCruiseSpeed(minimum_velocity, plot=False)


Shlimp = unpickle('Shlimp')
Shlimp.report()

# Shlimp = unpickle('Shlimp.txt')
# simulateVelocity(Shlimp, v0=Shlimp.cruiseV, throttle=0, tmax=50)
#Shlimp.report()
#plot_blimp(Shlimp)






