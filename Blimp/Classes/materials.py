class Material:
    def __init__(self, vol_density, area_density, E, tensile_strength):
        self.vol_density = vol_density            # [kg/m^3]
        self.area_density = area_density          # [kg/m^2]
        self.E = E                                # [Pa]
        self.tensile_strength = tensile_strength  # [Pa]



###############################
# MATERIAL LIBRARY
###############################

# Balloon Materials
test = Material(1, 300, 240)

# Structural Materials
