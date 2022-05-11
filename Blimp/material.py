class Material:
    def __init__(self, vol_density, E, tensile_strength):
        self.density = vol_density
        self.E = E
        self.tensile_strength = tensile_strength

###############################
# MATERIAL LIBRARY
###############################

Cellophane = Material(1, 300, 240)
