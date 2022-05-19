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

ZED_F9P = Electronic("ZED_F9P", mass=0.005, 0.204, 189.99, "GPS Module")


############################################
# List of possible electronic configurations
############################################

