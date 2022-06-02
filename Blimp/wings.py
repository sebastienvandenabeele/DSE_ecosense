import numpy as np


class Wing:
    def __init__(self, m_lift, v_cruise, ar=7.32, cl_cruise=0.7, skin_gsm=400, core_rho=35, airfoil_t=0.12):
        """
        Class describing wings (meant to lift the payload as a buoyancy
        control system, but should be universal)
        :param m_lift: [float] Mass to be lifted by the wings [kg]
        :param v_cruise: [float] Cruise velocity [m/s]
        :param ar: [float] Aspect ratio [-]
        Default AR = 7.32 taken from classic Cessna
        :param cl_cruise: [float] Cruise lift coefficient [-]
        Default cruise CL = 0.7 estimated from NACA2412
        :param skin_gsm: [float] Weight in gram per square meter of the covering skin [gsm]
        Default skin gsm = 400 gsm estimated just based on a higher weight CFRP prepreg.
        :param core_rho: [float] Density of the core material [kg/m^3]
        Default core rho = 35 kg/m^3 based on higher end of EPS density range.
        :param airfoil_t: [float] Max thickness of the airfoil used as a fraction of the chord [-]
        Default thickness = 12% based on NACA2412
        """
        self.rho = 1.225  # [kg/m3] SSL
        self.lift = 9.81 * m_lift  # [N] force
        self.v_cruise = v_cruise
        self.ar = ar
        self.cl_cruise = cl_cruise
        self.skin_rho = skin_gsm / 1000  # [kg/m^2]
        self.core_rho = core_rho
        self.airfoil_t = airfoil_t
        self.area, self.b, self.c = self.dimensions()
        self.mass = self.mass()

    def dimensions(self):
        """
        Determines the planform dimensions of the wing, assuming untapered, straight wings
        :return: [float, float, float] Area [m^2], Span [m], Chord [m]
        """
        s = self.lift * 2 / (self.rho * (self.v_cruise ** 2) * self.cl_cruise)
        b = np.sqrt(s * self.ar)
        c = b / self.ar
        return s, b, c

    def mass(self):
        """
        Determines weight of the wing, assuming it to be a sandwich panel with the same area
        as the wing and half of the max airfoil thickness throughout. Sides also covered with skin.
        :return: [float] Mass of the wing [kg]
        """
        # TODO: add servo and control surface mass
        m_skin = 2 * (self.area + (self.b * self.airfoil_t / 2)) * self.skin_rho
        m_core = 2 * self.area * (self.airfoil_t / 2) * self.core_rho
        return m_core + m_skin

    def print(self):
        """
        Function to print the properties of a wing.
        """
        print("Wing properties: \n Area: " + str(self.area) + " [m^2] \n Span: " +
              str(self.b) + " [m] \n Chord: " + str(self.c) + " [m] \n Mass: " + str(self.mass) + " [kg]")
