import numpy as np


class Fin:
    def __init__(self, root_chord, tip_chord, control_chord, span, taper_ratio, mass, surface, MAC, cg, AR):
        self.root_chord = root_chord
        self.tip_chord = tip_chord
        self.control_chord = control_chord
        self.span = span
        self.taper_ratio = taper_ratio
        self.mass = mass
        self.surface = surface
        self.MAC = MAC
        self.cg = cg
        self.AR = AR


def sizeControl(blimp):
    taper_ratio = 0.5  # ratio form blibble
    surface = 0.03265958005 / blimp.n_fins * \
        blimp.volume  # ratio from blibble airships
    fin_root = np.sqrt((2*surface*(1+taper_ratio)) /
                       (1+taper_ratio+taper_ratio**2))
    fin_tip = fin_root*taper_ratio
    # ratio from https://www.aero.iitb.ac.in/~ltasys/WEBPAGES/PDFs/npaper03.pdf
    control_root = 0.1978*fin_root
    span = (1+taper_ratio)*fin_root/2
    surface_ratio = (control_root*span)/surface

    MAC = fin_root * 2/3 * \
        ((1 + taper_ratio + taper_ratio**2) / (1 + taper_ratio))
    cg = 0.52*fin_root
    AR = span**2 / surface


    # first: ratio of control surfaces, second, third:coefficients from book
    mass_fin = 0.192*2*surface*(1-surface_ratio)*1.26*2.36
    # ratio, factor from book, conversion from lb to kg
    mass_control = surface*surface_ratio*0.3*4.88
    # ratio, factor from book, conversion, installation factor
    mass_actuator = surface*surface_ratio*0.08*4.88*1.15

    fin = Fin(fin_root, fin_tip, control_root, span, taper_ratio, sum(
        [mass_fin, mass_control, mass_actuator]), surface, MAC, cg, AR)
    return fin
