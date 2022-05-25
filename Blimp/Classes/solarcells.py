class Solarcell:
    def __init__(self, density, efficiency, width, length, area, fillfac, cost, Vmpp=0, Impp=0):
        """
        A class describing a solar cell type which can be used for the blimp
        :param density: [float] area density of solar cell [kg/m^2]
        :param efficiency: [float] solar panel efficiency (0.0-1.00) [-]
        :param width: [float] width of single solar cell [m]
        :param length: [float] length of single solar cell [m]
        :param area: [float] net area of single solar cell [m^2]
        :param fillfac: [float] fill factor, percentage of area used [-]
        :param cost: [float] unit cost of single solar cell [EUR]
        :param Vmpp: [float] Voltage at maximum power point [V]
        :param Impp: [float] Current at maximum power point [A]
        """
        self.density = density
        self.efficiency = efficiency
        self.width = width
        self.length = length
        self.area = area
        self.fillfac = fillfac
        self.cost = cost        #Unit cost in EUR


####################
# Solar Cell library
#####################

maxeon_gen3 = Solarcell(density=0.0425, efficiency=0.231, width=0.125, length=0.125, area=0.0153, fillfac=0.8, cost=3.33) #Ultra High Performance variant (conservative)


solarcells = [maxeon_gen3]