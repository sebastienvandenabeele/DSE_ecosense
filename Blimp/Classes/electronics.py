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

ZED_F9P = Electronic(name="ZED_F9P", mass=0.005, power_consumption=0.204, cost=189.99, type="GPS Module")
Honeywell_SATCOM = Electronic("Honeywell SATCOM", 0.994, 44, 2800, "TX/RX")
pixhawk = Electronic("Pixhawk 4", 0.0158, 2, 180, "FC")


############################################
# List of possible electronic configurations
############################################

