class Solarcell:
    def __init__(self, density, efficiency, width, length, area, fillfac, Vmpp=0, Impp=0):
        self.density = density
        self.efficiency = efficiency
        self.width = width
        self.length = length
        self.area = area
        self.fillfac = fillfac


    ####################
    # Solar Cell library
    #####################

maxeon_gen3 = Solarcell(0.0425, 0.231, 0.125, 0.125, 0.0153, 0.8) #Ultra High Performance variant (conservative)