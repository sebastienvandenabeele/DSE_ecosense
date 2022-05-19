class Electronic:
    def __init__(self, name, mass, power_consumption, cost, voltage):
        """
        A class describing any secondary electronic component
        :param: name: [str] Name of component
        :param mass: [float] Mass of component [kg]
        :param power_consumption: [float] Steady-state power consumption [W]
        :param cost: [float] Unit cost of component [EUR]
        :param voltage: [float] Voltage of component [V]
        """

        self.name = name
        self.mass = mass
        self.power_consumption = power_consumption
        self.cost = cost
        self.voltage = voltage


#####################
# Electronics library
#####################


############################################
# List of possible electronic configurations
############################################

