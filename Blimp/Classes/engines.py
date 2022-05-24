import numpy as np
from matplotlib import pyplot as plt

class Engine:
    instances = set()
    std_safe_thr = 0.55

    def __init__(self, mfg, name, max_power, mass, n_cells, prop_diameter, KV, cost, safe_thr=std_safe_thr, efficiency=0.80):
        """
        A class describing electrical motors used for propulsion
        :param mfg: [str] Name of manufacturer [-]
        :param name: [str] Name of the motor [-]
        :param max_power: [float] Maximum power at 100% throttle [W]
        :param mass: [float] Mass including everything needed to operate the engine [g]
        :param n_cells: [int] (Max) number of cells (3.7V-4.2V per cell) [-]
        :param prop_diameter: [float] (Max) diameter of the biggest recommended propeller [inch]
        :param KV: [int] KV rating (RPM/V applied) [-]
        :param cost: [float] Cost of unit [EUR]
        :param safe_thr: [float] Safe throttle setting [%]
        :param efficiency: [float] Maximum throttle the engine operates at (from 0.0 - 1.0)
        """
        

        self.mfg = mfg
        self.name = name
        self.max_power = max_power
        self.mass = mass / 1000  # conv. g to kg
        self.n_cells = n_cells
        self.prop_diameter = prop_diameter / 2.54 / 100  # conv. inch to m
        self.KV = KV
        self.cost = cost
        self.safe_thr = safe_thr
        self.efficiency = efficiency

        self.__class__.instances.add(self)

##################
# Engine Library

# Template:
# = Engine(mfg=, name=, max_power=, mass=, n_cells=, prop_diameter=, KV=, cost=)

# For all KV variants, the "name" parameter should be the same
##################

# T-motor
# FPV
tmt_f60prov_1750 = Engine(mfg="tmt", name="F60PROV", max_power=1003, mass=34.3, n_cells=6, prop_diameter=5, KV=1750, cost=25.7)
tmt_f60prov_1950 = Engine(mfg="tmt", name="F60PROV", max_power=1216, mass=33.9, n_cells=6, prop_diameter=5, KV=1950, cost=25.7)
tmt_f60prov_2020 = Engine(mfg="tmt", name="F60PROV", max_power=1297, mass=33.8, n_cells=6, prop_diameter=5, KV=2020, cost=25.7)
tmt_f60prov_2550 = Engine(mfg="tmt", name="F60PROV", max_power=825, mass=33.3, n_cells=4, prop_diameter=5, KV=2550, cost=25.7)
tmt_1104_7500 = Engine(mfg="tmt", name="1104", max_power=198, mass=5.6, n_cells=4, prop_diameter=3, KV=7500, cost=11.3)
tmt_0803_22000 = Engine(mfg="tmt", name="0803", max_power=22.7, mass=2.47, n_cells=1, prop_diameter=1, KV=22000, cost=10.4)
tmt_1404_2900 = Engine(mfg="tmt", name="1404", max_power=262, mass=9.34, n_cells=6, prop_diameter=4, KV=2900, cost=16.1)
tmt_1404_3800 = Engine(mfg="tmt", name="1404", max_power=304, mass=9.34, n_cells=4, prop_diameter=4, KV=3800, cost=16.1)
tmt_1404_4600 = Engine(mfg="tmt", name="1404", max_power=316, mass=9.34, n_cells=4, prop_diameter=4, KV=4600, cost=16.1)
tmt_2307_1950 = Engine(mfg="tmt", name="2307", max_power=974, mass=35.1, n_cells=6, prop_diameter=5, KV=1950, cost=16.7)
tmt_2307_1950 = Engine(mfg="tmt", name="2307", max_power=534, mass=35.5, n_cells=5, prop_diameter=5, KV=2550, cost=16.7)
tmt_f1000_510 = Engine(mfg="tmt", name="F1000", max_power=4000, mass=404, n_cells=8, prop_diameter=13, KV=510, cost=114.2)
tmt_f1000_300 = Engine(mfg="tmt", name="F1000", max_power=4548, mass=400, n_cells=12, prop_diameter=13, KV=300, cost=114.2)
# Fixed wing
tmt_2303_1500 = Engine(mfg="tmt", name="2303", max_power=100, mass=18, n_cells=3, prop_diameter=10, KV=1500, cost=34.3, safe_thr=0.75)
tmt_2303_1800 = Engine(mfg="tmt", name="2303", max_power=70, mass=18, n_cells=2, prop_diameter=9, KV=1800, cost=34.3, safe_thr=0.8)
tmt_2303_2300 = Engine(mfg="tmt", name="2303", max_power=65, mass=18, n_cells=2, prop_diameter=7, KV=2300, cost=34.3, safe_thr=0.85)
tmt_2321_950 = Engine(mfg="tmt", name="2321", max_power=450, mass=93, n_cells=4, prop_diameter=12, KV=950, cost=42.8, safe_thr=0.7)
tmt_2321_1250 = Engine(mfg="tmt", name="2321", max_power=700, mass=94, n_cells=4, prop_diameter=11, KV=1250, cost=42.8)
tmt_4130_230 = Engine(mfg="tmt", name="4130", max_power=2500, mass=408, n_cells=12, prop_diameter=17, KV=230, cost=114.2)
tmt_4130_300 = Engine(mfg="tmt", name="4130", max_power=3200, mass=405, n_cells=12, prop_diameter=18, KV=300, cost=114.2)
tmt_4130_450 = Engine(mfg="tmt", name="4130", max_power=1800, mass=408, n_cells=6, prop_diameter=18, KV=450, cost=114.2)

# TPPower
tpp_3640_2080 = Engine(mfg="tmt", name="3640", max_power=2800, mass=322, n_cells=6, prop_diameter=7, KV=2080, cost=139)


# powers = [eng.max_power for eng in Engine.instances]
# weights = [eng.mass for eng in Engine.instances]
# plt.scatter(powers, weights)
# plt.grid()
# plt.xlabel('Power [W]')
# plt.ylabel('Weight [kg]')
# plt.show()

weight_per_W = np.mean([eng.mass / eng.max_power for eng in Engine.instances])
weight_per_W = 0.0001166666  # manual adaption
