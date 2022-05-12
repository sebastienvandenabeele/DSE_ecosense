class Gas:
    R = 8.3145  # ideal gas constant
    pres_std = 101325  # Pa
    temp_std = 273.15  # K

    def __init__(self, m_molar, temp, pres, spec_energy):
        """
        :param m_molar: Molar mass [kg/mol]
        :param temp: Temperature [K]
        :param pres: Pressure [Pa]
        """
        self.m_molar = m_molar
        self.temp = temp
        self.pres = pres
        self.dens = (self.pres * self.m_molar)/(self.temp * Gas.R)  # ideal gas law

        self.spec_energy = spec_energy # [J/m3]

##############
# Gas library
##############

hydrogen = Gas(0, 0, 0, 10800000)
