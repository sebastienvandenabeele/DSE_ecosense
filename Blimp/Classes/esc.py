class ESC:
    def __init__(self, mfg, name, mass, cost, max_amp, n_motors, n_cells, bec=False):
        """
        A class describing electronic speed controllers for motors
        :param mfg: [str] Name of manufacturer
        :param name: [str] Name of component
        :param mass: [float] Mass of component [kg]
        :param cost: [float] Unit cost of component [EUR]
        :param max_amp: [float] Maximum amperage [A]
        :param n_motors: [int] Number of motors supported
        :param n_cells: [int] Number of cells
        :param bec: [bool] Does the esc have a 5V output?
        """
        self.mfg = mfg
        self.name = name
        self.mass = mass
        self.cost = cost
        self.max_amp = max_amp
        self.n_motors = n_motors
        self.n_cells = n_cells


escs = []
# escs.append(ESC(mfg=, name=, mass=, cost=, max_amp=, n_motors=, n_cells=))

# T-motor
# fixed wing
escs.append(ESC(mfg="tmt", name="AT12A", mass=11, cost=10, max_amp=12, n_motors=1, n_cells=3, bec=True))
escs.append(ESC(mfg="tmt", name="AT20A", mass=19, cost=11, max_amp=20, n_motors=1, n_cells=3, bec=True))
escs.append(ESC(mfg="tmt", name="AT30A", mass=37, cost=13, max_amp=30, n_motors=1, n_cells=3, bec=True))
escs.append(ESC(mfg="tmt", name="AT40A", mass=43, cost=15, max_amp=40, n_motors=1, n_cells=4, bec=True))
escs.append(ESC(mfg="tmt", name="AT55A", mass=63, cost=30, max_amp=55, n_motors=1, n_cells=6, bec=True))
escs.append(ESC(mfg="tmt", name="AT75A", mass=82, cost=35, max_amp=75, n_motors=1, n_cells=6, bec=True))
escs.append(ESC(mfg="tmt", name="AT115A", mass=182, cost=110, max_amp=115, n_motors=1, n_cells=14, bec=True))
# Alpha series
escs.append(ESC(mfg="tmt", name="ALPHA40A6S", mass=54.5, cost=65, max_amp=40, n_motors=1, n_cells=6))
escs.append(ESC(mfg="tmt", name="ALPHA60A6S", mass=62.8, cost=65, max_amp=60, n_motors=1, n_cells=6))
escs.append(ESC(mfg="tmt", name="ALPHA60A12S", mass=73, cost=105, max_amp=60, n_motors=1, n_cells=12))
escs.append(ESC(mfg="tmt", name="ALPHA60A24S", mass=360, cost=270, max_amp=40, n_motors=1, n_cells=24))
escs.append(ESC(mfg="tmt", name="ALPHA80A12S", mass=110, cost=120, max_amp=80, n_motors=1, n_cells=12))
escs.append(ESC(mfg="tmt", name="ALPHA120A12S", mass=360, cost=155, max_amp=100, n_motors=1, n_cells=12))

