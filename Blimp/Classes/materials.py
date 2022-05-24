from re import M


class Material:

    def __init__(self, density=0, price_kg = 0, E=0, tensile_strength=0, elongation = 0, shear_mod = 0, fatigue = 0,
                 hard = 0, rup_mod = 0, UV = 0, water_res = 0, C02_mat = 0, C02_proc = 0, recycle = 0, biodegrade = 0):
        """
        A class defining materials 
        :param density: [float] Volumetric density of material [kg/m^3]
        :param price_kg: [float] price in euros per kg of material
        :param E: [float] Young's modulus of material [GPA]
        :param Y: [float] yield strength in [GPA]
        :param tensile_strength: [float] Tensile strength of material [MPa]
        :param elongation: [float] strain of material in %
        :param shear_mod: [float] shear modulus in GPA
        :param fatigue: [float] fatigue strength at 10^7 cycles in MPA
        :param hard: [float] Hardness in HV
        :param rup_mod: [float] modulus of rupture in MPA
        :param UV: [string] UV resistance # (days/weeks, months/years, years, ten years)
        :param water_res: [string] water resistance # (unacceptable,limited use,acceptable, excellent)
        :param C02_mat: [value] C02 produced to create 1kg of material in kg/kg
        :param C02_proc: [value] CO2 footprint associated with processing in kg/kg (prepreg + fabric)
        :param recycle: [Bool] material recyclable # True or False
        :param biodegrade: [Bool] material biodegradable 
        
        """
        self.density = density # max density kg/m^3
        self.price_kg = price_kg       # max price in Euro/kg
        self.E = E             # min E in Pa
        self.tensile_strength = tensile_strength * 10**6 / 4 # min tensile strength from MPa to Pa
        # TODO: all the material definitiions are UD. For now, the strength is divided by 4 but this is not sufficient.
        self.elongation = elongation   # maximum elongation in %
        self.shear_mod = shear_mod    # min shear modulus in GPA
        self.fatigue = fatigue        # min fatigue in MPA
        self.hard = hard               # min in HV
        self.rup_mod = rup_mod        # min in MPA
        self.UV = UV
        self.water_res = water_res
        self.C02_mat = C02_mat        # max kg
        self.C02_proc = C02_proc      # max kg
        self.recycle = recycle
        self.biodegrade = biodegrade




###############################
# MATERIAL LIBRARY
###############################

#<<<<<<< HEAD
# load carrying materials
Kevlar_K149 = Material(
    price_kg = 203,
    density= 1480,
    E= 170, 
    tensile_strength= 3200, 
    elongation = 1.3,
    shear_mod = 1,
    fatigue = 2500,
    hard = 25,
    rup_mod = 2500, 
    UV = "Fair", 
    water_res = "Acceptable", 
    C02_mat = 18.2, 
    C02_proc = 3.6, 
    recycle = False,
    biodegrade = False
)
cotton_fiber = Material(
    price_kg = 4.72,
    density= 1560,
    E= 7, 
    tensile_strength= 360, 
    elongation = 11,
    shear_mod = 1,
    fatigue = 0,
    hard = 0,
    rup_mod = 300, 
    UV = "Fair", 
    water_res = "Acceptable", 
    C02_mat = 0.94, 
    C02_proc = 0.218, 
    recycle = False,
    biodegrade = True
)

jute_fiber = Material(
    price_kg = 0.308,
    density= 1520,
    E= 17, 
    tensile_strength= 400, 
    elongation = 1.7,
    shear_mod = 6.3,
    fatigue = 160,
    hard = 0,
    rup_mod = 400, 
    UV = "Good", 
    water_res = "Acceptable", 
    C02_mat = 2.96, 
    C02_proc = 0.218, 
    recycle = False,
    biodegrade = True
)

Kenaf_fiber = Material(
    price_kg = 0.507,
    density= 980,
    E= 35, 
    tensile_strength= 390, 
    elongation = 2,
    shear_mod = 12.9,
    fatigue = 156,
    hard = 0,
    rup_mod = 390, 
    UV = "Good", 
    water_res = "Acceptable", 
    C02_mat = 0.218, 
    C02_proc = 1.46, 
    recycle = False,
    biodegrade = True
)

# poly amids (nylon)

# PA66_40carbon = Material(
#     price_kg = 13.8,
#     vol_density= 1350, 
#     E= 29, 
#     tensile_strength= 297, 
#     elongation = 1,
#     shear_mod = 12.3,
#     fatigue = 78.4,
#     hard = 0,
#     rup_mod = 414, 
#     UV = "Poor", 
#     water_res = "Excellent", 
#     C02_mat = 34.9, 
#     C02_proc = 8.7, 
#     recycle = False
#     biodegrade = False

# )

PBO_fiber = Material(
    price_kg = 162,
    density= 1560,
    E= 180, 
    tensile_strength= 5680, 
    elongation = 2.5,
    shear_mod = 12.3,
    fatigue = 78.4,
    hard = 0,
    rup_mod = 5680, 
    UV = "Poor", 
    water_res = "", #?
    C02_mat = 20.2, 
    C02_proc = 0.218, 
    recycle = False,
    biodegrade = False

)

polyamide_fiber = Material(
    price_kg = 2.84,
    density= 1150,
    E= 4, 
    tensile_strength= 600, 
    elongation = 16,
    shear_mod = 1,
    fatigue = 0, #?
    hard = 0, #?
    rup_mod = 600, 
    UV = "Fair", 
    water_res = "Excellent", 
    C02_mat = 8.1, 
    C02_proc = 0.218, 
    recycle = True,
    biodegrade = False

)

polyarylate_fiber = Material(
    price_kg = 33.5,
    density= 1400,
    E= 55, 
    tensile_strength= 2900, 
    elongation = 2.8,
    shear_mod = 6,
    fatigue = 0, #?
    hard = 0, #?
    rup_mod = 2900, 
    UV = "Good", 
    water_res = "Excellent", 
    C02_mat = 8.1, 
    C02_proc = 0.218, 
    recycle = True,
    biodegrade = False
)

Dacron = Material(
    price_kg = 1.32,
    density= 1390,
    E= 3, 
    tensile_strength= 573, 
    elongation = 18,
    shear_mod = 1,
    fatigue = 0, #?
    hard = 0, #?
    rup_mod = 573, 
    UV = "Good", 
    water_res = "Excellent", 
    C02_mat = 4.7, 
    C02_proc = 0.218, 
    recycle = True,
    biodegrade = False
)

# Dyneema
polyethylene_fiber = Material(
    price_kg = 110,
    density= 975,
    E= 120, 
    tensile_strength= 2900,
    elongation = 2.9,
    shear_mod = 0.3,
    fatigue = 2500,
    hard = 5,
    rup_mod = 2500, 
    UV = "Good", 
    water_res = "Excellent", 
    C02_mat = 23.5, 
    C02_proc = 0.218, 
    recycle = False,
    biodegrade = False
)






# Epoxy/HS carbon fiber, woven prepreg,biaxial lay-up
# Flax fiber
# hard rubber (ebonite)
# hemp fiber



# sealant material




# materials for payload bay


#=======
# Balloon Materials
#>>>>>>> 7b3223617bfcd5d9775bd1cb0feaaf440573f9ba

# Structural Materials
