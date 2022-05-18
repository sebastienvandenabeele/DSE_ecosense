class Electronic:
    def __init__(self, name, mass, power_consumption, cost):
        """
        A class describing any secondary electronic component
        :param: name: [str] Name of component
        :param mass: [float] Mass of component [kg]
        :param power_consumption: Steady-state power consumption [W]
        :param cost: Unit cost of component [EUR]
        """

        self.name = name
        self.mass = mass
        self.power_consumption = power_consumption
        self.cost = cost


#####################
# Electronics library
#####################


############################################
# List of possible electronic configurations
############################################

