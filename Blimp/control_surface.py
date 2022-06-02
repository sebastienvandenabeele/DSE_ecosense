import numpy as np

def sizeControl(blimp, report=False):
    taper_ratio=0.5 #ratio form blibble
    surface= 0.03265958005 / blimp.n_fins * blimp.volume # ratio from blibble airships
    fin_root=np.sqrt((2*surface*(1+taper_ratio))/(1+taper_ratio+taper_ratio**2))
    fin_tip=fin_root*taper_ratio
    control_root=0.1978*fin_root #ratio from https://www.aero.iitb.ac.in/~ltasys/WEBPAGES/PDFs/npaper03.pdf
    control_tip=control_root
    span=(1+taper_ratio)*fin_root/2
    surface_ratio=(control_root*span)/surface

    if report:
        print('Fin root', fin_root)
        print('Fin tip', fin_tip)


    
    mass_fin=0.192*2*surface*(1-surface_ratio)*1.26*2.36 # first: ratio of control surfaces, second, third:coefficients from book 
    mass_control=surface*surface_ratio*0.3*4.88  #ratio, factor from book, conversion from lb to kg
    mass_actuator=surface*surface_ratio*0.08*4.88*1.15 #ratio, factor from book, conversion, installation factor
    return sum([blimp.n_fins * mass_fin, blimp.n_fins * mass_control, blimp.n_fins * mass_actuator]), surface, fin_root



