class Gas:
    R = 8.3145  # ideal gas constant
    pres_std = 101325  # Pa
    temp_std = 273.15  # K

    def __init__(self, m_molar, temp, pres, spec_energy, cost):
        """
        :param m_molar: Molar mass [kg/mol]
        :param temp: Temperature [K]
        :param pres: Pressure [Pa]
        """
        self.m_molar = m_molar
        self.temp = temp
        self.pres = pres
        self.dens = (self.pres * self.m_molar)/(self.temp * Gas.R)  # ideal gas law
        self.spec_energy = spec_energy  # [J/m3]
        self.cost = cost  # [EUR / m^3]


##############
# Gas library
##############

hydrogen = Gas(m_molar=0.00201568, pres=Gas.pres_std, temp=Gas.temp_std, spec_energy=10800000, cost=0.66)  # dens = 0.088
air = Gas(m_molar=0.027457, pres=Gas.pres_std, temp=Gas.temp_std, spec_energy=0, cost=0)  # dens = 1.225
