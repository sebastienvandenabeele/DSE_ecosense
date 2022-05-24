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
HGLRC_M80= Electronic(name="HGLRC_M80", mass=0.0094, power_consumption=0.0825, cost=20, type="GPS Module")

    # Small range
ultrasonic = Electronic(name="HC-SR04", mass=0.0085, power_consumption=0.075, cost=4.5, type="Ultrasonic Module")
lidar = Electronic (name="LiDAR", mass=0.011, power_consumption=0.55, cost=50, type="LiDAR")


# Communication modules
Honeywell_SATCOM = Electronic(name="Honeywell SATCOM", mass=0.994, power_consumption=44, cost=2800, type="TX/RX")


# Flight Controllers
pixhawk = Electronic(name="Pixhawk 4", mass=0.0158, power_consumption=2, cost=180, type="Flight Controller")
skynode = Electronic(name="'Auterion Skynode", mass=0.188, power_consumption=11, cost=1490, type="Flight Controller")


# Batteries



############################################
# List of possible electronic configurations
############################################
config_first_order = [NEO_M9N, lidar, Honeywell_SATCOM, pixhawk]