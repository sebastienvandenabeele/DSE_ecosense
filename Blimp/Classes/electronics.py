#from pyrsistent import T


class Electronic:
    def __init__(self, name, mass, type, constant_power_consumption=0.0, partial_power_consumption=0.0, cost=0.0):
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
        self.constant_power_consumption = constant_power_consumption
        self.partial_power_consumption = partial_power_consumption
        self.cost = cost
        self.type = type


#####################
# Electronics library
#####################

# GPS Modules
    # Big range
ZED_F9P = Electronic(name="ZED_F9P", mass=0.005, constant_power_consumption=0.204, cost=189.99, type="GPS Module") # doesn't need small range module
NEO_M9N = Electronic(name="NEO-M9N", mass=0.0016, constant_power_consumption=0.108, cost=70, type="GPS Module")
HGLRC_M80 = Electronic(name="HGLRC_M80", mass=0.0094, constant_power_consumption=0.0825, cost=20, type="GPS Module")

    # Small range
ultrasonic = Electronic(name="HC-SR04", mass=0.0085, constant_power_consumption=0.075, cost=4.5, type="Ultrasonic Module")
lidar = Electronic (name="LiDAR", mass=0.011, constant_power_consumption=0.55, cost=50, type="LiDAR")


# Communication modules
Honeywell_SATCOM = Electronic(name="Honeywell SATCOM", mass=0.994, constant_power_consumption=44, cost=2800, type="TX/RX")


# Flight Controllers
pixhawk = Electronic(name="Pixhawk 4", mass=0.0158, constant_power_consumption=2, cost=180, type="Flight Controller")
skynode = Electronic(name="'Auterion Skynode", mass=0.188, constant_power_consumption=25, cost=1490, type="Flight Controller")


# Batteries
lion_battery = Electronic(name="Li-ion battery", mass=0.0485, constant_power_consumption=0, cost=4.35, type="Battery") # Capacity: 3450mAh, Volume: 3.6V - 3.7V
# 12*7 battery pack:
battery_pack = Electronic(name="Battery Pack", mass=12*7*lion_battery.mass, constant_power_consumption=0, cost=12*7*lion_battery.cost, type="Battery Pack")


# Solar Charge Controllers
custom_scc = Electronic(name="Arduino MPPT Solar Charge Controller", mass=0.1, constant_power_consumption=0, cost=100, type="Solar Charge Controller") # 1kW
smart_solar_1 = Electronic(name="SmartSolar Laadcontroller MPPT 150/45", mass=1.25, constant_power_consumption=0, cost=472, type="Solar charger") # 2.6kW
smart_solar_2 = Electronic(name="SmartSolar Laadcontroller MPPT 250/70", mass=3, constant_power_consumption=0, cost=907, type="Solar charger") # 4kW
smart_solar_3 = Electronic(name="SmartSolar Laadcontroller MPPT 100/20", mass=0.65, constant_power_consumption=0, cost=160, type="Solar charger") # 1.16kW
solar_pack_1 = Electronic(name="Solar pack 1", mass=smart_solar_1.mass*3, constant_power_consumption=0, cost=smart_solar_1.cost*3, type="Solar pack") # 2.6kW*3 = 7.8kW
solar_pack_2 = Electronic(name="Solar pack 2", mass=smart_solar_2.mass*2, constant_power_consumption=0, cost=smart_solar_2.cost*2, type="Solar pack") # 4kW*2 = 8kW
solar_pack_3 = Electronic(name="Solar pack 3", mass=smart_solar_3.mass*7, constant_power_consumption=0, cost=smart_solar_3.cost*7, type="Solar pack") # 1.16kW*7 = 8.12kW


# Deployment components
EM = Electronic(name="PEM1213A", mass=0.01, partial_power_consumption=1, cost=7, type="Electromagnet") 
motion_sensor = Electronic(name="Quad-Beam Photoelectric Sensor", mass=2.27, constant_power_consumption=5, cost=119, type="Motion Sensor")
photoresistor = Electronic(name="GL5516 LDR", mass=0.00025, cost=0.15, type="Servo")
mass_flow_sensor = Electronic(name="Auto Mass Air Flow Sensor Meter", mass=0.45, cost=75, type="Mass flow sesnsor")

# Fin and propulsion actuators
MEGAservo = Electronic(name="HS-5805MG Mega", mass=0.197, constant_power_consumption=0.003, partial_power_consumption=15, cost=77, type="Servo")

# Pressure and H2 sensors
pressure_sensor = Electronic(name="MPX 2200DP", mass=0.05, cost=17.54, type="Pressure Sensor")
H2_sensor = Electronic(name="H2-AF", mass=0.04, cost=30, type="H2 sensor")


# Altitude Control actuators


# Venting and Ballonet
#air_valve = Electronic(name="Electric Solenoid Air Valve", mass=0.141, constant_power_consumption=0, cost=8.85, type="Air Value")
valve = Electronic(name="2 Way Solenoid Valve", mass=0.235, partial_power_consumption=19, cost=283.68, type="Valve")
fan = Electronic(name='Ballonet Fan', mass=0.08, partial_power_consumption=19.2, cost=26.9, type='Fan')


############################################
# List of possible electronic configurations
############################################

# 8kW system config
config_option_1 = [ZED_F9P, Honeywell_SATCOM, skynode, smart_solar_2, fan] + [valve]*3 + [MEGAservo]*8 + 2*[pressure_sensor] + 2*[H2_sensor] + 551*[photoresistor] + 2*[mass_flow_sensor]

elec_cost = 0
elec_mass = 0
elec_powercons = 0
max_power = 0

# print(config_option_1)

for item in config_option_1:
    elec_cost += item.cost
    elec_mass += item.mass
    elec_powercons += item.constant_power_consumption
    max_power += item.constant_power_consumption + item.partial_power_consumption


print(elec_cost, elec_mass, elec_powercons, max_power)

