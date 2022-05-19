class Material:

    def __init__(self, vol_density=0, area_density=0, E=0, tensile_strength=0):
        """
        A class defining materials
        :param vol_density: [float] Volumetric density of material [kg/m^3]
        :param area_density: [float] Area density of material [kg/m^2]
        :param E: [float] Young's modulus of material [GPa]
        :param tensile_strength: [float] Tensile strength of material [MPa]
        """
        self.vol_density = vol_density
        self.area_density = area_density
        self.E = E / 10**9                               # conversion to Pa
        self.tensile_strength = tensile_strength / 10**6   # conversion to Pa



###############################
# MATERIAL LIBRARY
###############################

# Balloon Materials

# Structural Materials
