from pyrsistent import T


class Electronic:
    def __init__(self, name, mass, power_consumption, cost, type):
        """
        A class describing any secondary electronic component
        :param: name: [str] Name of component
        :param mass: [float] Mass of component [kg]
        :param power_consumption: Steady-state power consumption [W]
        :param cost: Unit cost of component [EUR]
        :param type: [str] Type of the component 
        """

        self.name = name
        self.mass = mass
        self.power_consumption = power_consumption
        self.cost = cost
        self.type = type


#####################
# Electronics library
#####################

# GPS Modules
    # Big range
ZED_F9P = Electronic(name="ZED_F9P", mass=0.005, power_consumption=0.204, cost=189.99, type="GPS Module") # doesn't need small range module
NEO_M9N = Electronic(name="NEO-M9N", mass=0.0016, power_consumption=0.108, cost=70, type="GPS Module")
HGLRC_M80 = Electronic(name="HGLRC_M80", mass=0.0094, power_consumption=0.0825, cost=20, type="GPS Module")

    # Small range
ultrasonic = Electronic(name="HC-SR04", mass=0.0085, power_consumption=0.075, cost=4.5, type="Ultrasonic Module")
lidar = Electronic (name="LiDAR", mass=0.011, power_consumption=0.55, cost=50, type="LiDAR")


# Communication modules
Honeywell_SATCOM = Electronic(name="Honeywell SATCOM", mass=0.994, power_consumption=44, cost=2800, type="TX/RX")


# Flight Controllers
pixhawk = Electronic(name="Pixhawk 4", mass=0.0158, power_consumption=2, cost=180, type="Flight Controller")
skynode = Electronic(name="'Auterion Skynode", mass=0.188, power_consumption=11, cost=1490, type="Flight Controller")


# Batteries
lion_battery = Electronic(name="Li-ion battery", mass=0.0485, power_consumption=0, cost=4.35, type="Battery") # Capacity: 3450mAh, Volume: 3.6V - 3.7V
# 12*7 battery pack:
battery_pack = Electronic(name="Battery Pack", mass=12*7*lion_battery.mass, power_consumption=0, cost=12*7*lion_battery.cost, type="Battery Pack")


# Solar Charge Controllers
custom_scc = Electronic(name="Arduino MPPT Solar Charge Controller", mass=0.1, power_consumption=0, cost=100, type="Solar Charge Controller") # 1kW
smart_solar_1 = Electronic(name="SmartSolar Laadcontroller MPPT 150/45", mass=1.25, power_consumption=0, cost=472, type="Solar charger") # 2.6kW
smart_solar_2 = Electronic(name="SmartSolar Laadcontroller MPPT 250/70", mass=3, power_consumption=0, cost=907, type="Solar charger") # 4kW
smart_solar_3 = Electronic(name="SmartSolar Laadcontroller MPPT 100/20", mass=0.65, power_consumption=0, cost=160, type="Solar charger") # 1.16kW
solar_pack_1 = Electronic(name="Solar pack 1", mass=smart_solar_1.mass*3, power_consumption=0, cost=smart_solar_1.cost*3, type="Solar pack") # 2.6kW*3 = 7.8kW
solar_pack_2 = Electronic(name="Solar pack 2", mass=smart_solar_2.mass*2, power_consumption=0, cost=smart_solar_2.cost*2, type="Solar pack") # 4kW*2 = 8kW
solar_pack_3 = Electronic(name="Solar pack 3", mass=smart_solar_3.mass*7, power_consumption=0, cost=smart_solar_3.cost*7, type="Solar pack") # 1.16kW*7 = 8.12kW

# Fin and propulsion actuators
# Altitude Control actuators


# Valve actuators for venting system
air_valve = Electronic(name="Electric Solenoid Air Valve", mass=0.141, power_consumption=0, cost=8.85, type="Air Value")


############################################
# List of possible electronic configurations
############################################

# 8kW system config
config_option_1 = [ZED_F9P, Honeywell_SATCOM, skynode, solar_pack_2, air_valve, battery_pack] # Costas favourite one
config_option_2 = [NEO_M9N, ultrasonic, Honeywell_SATCOM, skynode, solar_pack_1, air_valve, battery_pack]
config_option_3 = [NEO_M9N, lidar, Honeywell_SATCOM, skynode, solar_pack_3, air_valve, battery_pack]
