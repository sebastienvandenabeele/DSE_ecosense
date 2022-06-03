import math


class Cell:
    def __init__(self, name, capacity, v_nominal, max_discharge, mass, cost):
        """
        Battery cell class. Mostly LI-ION 18650 cells are expected to be used.
        :param name: [string] Name of cell [-]
        :param capacity: [float] Capacity of the battery [mAh]
        :param v_nominal: [float] Nominal voltage [V]
        :param max_discharge: [float] Maximum discharge rate [A]
        :param mass: [float] Mass of cell [g]
        :param cost: [float] Cost of cell [eur]
        """
        self.name = name
        self.capacity = capacity * v_nominal * 3.6  # [J]
        self.v_nominal = v_nominal  # [V]
        self.max_discharge = max_discharge * v_nominal  # [W]
        self.mass = mass / 1000  # [kg]
        self.cost = cost  # [eur]


class BatteryPack:
    def __init__(self, req_capacity, dod=0.9, req_discharge_rate=0, sf_discharge_rate=1.5):
        """
        Battery pack class, describes the configuration of cells required to fulfil requirements
        :param req_capacity: [float] Required capacity. Watch the unit. [J]
        :param dod: [float] Depth of discharge, fraction of capacity actually used [-]
        Default dod is 0.9
        :param req_discharge_rate: [float] Max. required discharge power [W]
        Default req. discharge rate is 0 in case non-d.r. limited options want to be considered.
        :param sf_discharge_rate: [float] Safety factor of discharge rate [-]
        Default SF is 1.5
        """
        self.discharge_rate = req_discharge_rate  # [W]
        self.sf_discharge_rate = sf_discharge_rate  # [-]
        self.capacity = req_capacity  # [J]
        self.dod = dod  # [-]
        self.cell, self.n_cells, self.dr_limited = self.create_pack()
        self.mass = self.n_cells * self.cell.mass
        self.cost = self.n_cells * self.cell.cost

    def create_pack(self, print_options=False):
        """
        Constructs a pack from the given requirements.
        :param print_options: [bool] Allows to print all options considered. Default off. [-]
        :return: [Cell, int, bool] Selected cell, number of cells, is pack limited by discharge rate?
        """
        pack_masses = []
        pack_dr_limited = []
        for cell in cell_library:
            # Compare cells required for cap. and discharge to see what factor is limiting
            n_cells_dr = math.ceil((self.discharge_rate * self.sf_discharge_rate) / cell.max_discharge)
            n_cells_cap = math.ceil((self.capacity / self.dod) / cell.capacity)
            if n_cells_dr > n_cells_cap:
                pack_dr_limited.append(True)
            else:
                pack_dr_limited.append(False)
            n_cells = max(n_cells_cap, n_cells_dr)
            pack_masses.append(n_cells * cell.mass)

            if print_options:
                print(cell.name + " pack has " + str(n_cells) + " cells, mass of " +
                      "{:.2f}".format(n_cells * cell.mass) + " kg and costs " + "{:.2f}".format(n_cells * cell.cost) +
                      " eur. D.r. limited: " + str(pack_dr_limited[-1]))

        min_mass_index = pack_masses.index(min(pack_masses))
        selected_cell = cell_library[min_mass_index]
        dr_limited = pack_dr_limited[min_mass_index]
        n_cells = int(pack_masses[min_mass_index] / selected_cell.mass)
        return selected_cell, n_cells, dr_limited


###########################
# Cell Library

# Template:
# Cell(name=, capacity=, v_nominal=, max_discharge=, mass=, cost=)

# Source for data: NKON.nl
# Costs assume 200 cells if discount available
###########################

cell_library = []

# Sony/Murata
# 18650
cell_library.append(Cell(name="vtc6", capacity=3000, v_nominal=3.6, max_discharge=30, mass=46.6, cost=7.5))
cell_library.append(Cell(name="vtc5d", capacity=2800, v_nominal=3.6, max_discharge=35, mass=47, cost=7.95))
cell_library.append(Cell(name="vtc5a", capacity=2600, v_nominal=3.6, max_discharge=35, mass=48, cost=6.6))
# 21700
cell_library.append(Cell(name="vtc6a", capacity=4000, v_nominal=3.6, max_discharge=40, mass=72.7, cost=7.55))

# Samsung
cell_library.append(Cell(name="s20s", capacity=2000, v_nominal=3.6, max_discharge=30, mass=46.3, cost=4.95))

# Molicel
cell_library.append(Cell(name="p28a", capacity=2800, v_nominal=3.6, max_discharge=35, mass=46, cost=4.69))
