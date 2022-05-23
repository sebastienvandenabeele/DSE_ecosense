class Engine:
    def __init__(self, name, max_power, mass, voltage, prop_diameter, KV, cost, efficiency=0.8):
        """
        A class describing electrical motors used for propulsion
        :param name: [str] Name of the motor [-]
        :param max_power: [float] Maximum power at 100% throttle [W]
        :param mass: [float] Mass including everything needed to operate the engine [g]
        :param voltage: [float] Operating voltage [V]
        :param prop_diameter: [float] Diameter of the biggest recommended propeller [inch]
        :param KV: [int] KV rating (RPM/V applied) [-]
        :param cost: [float] Cost of unit [EUR]
        :param efficiency: [float] Maximum throttle the engine operates at (from 0.0 - 1.0)
        """

        self.name = name
        self.max_power = max_power
        self.mass = mass / 1000 # conv. g to kg
        self.voltage = voltage
        self.prop_diameter = prop_diameter / 2.54 / 100  # conv. inch to m
        self.KV = KV
        self.cost = cost
        self.efficiency = efficiency

##################
# Engine Library

# Template:
# = Engine(name=, max_power=, mass=, voltage=, prop_diameter=, KV=, cost=)

# For all KV variants, the "name" parameter should be the same
##################

# T-motor

# Axi