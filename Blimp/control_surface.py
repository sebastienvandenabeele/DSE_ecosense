# import numpy as np
# import matplotlib.pyplot as plt
import scipy.integrate as integrate

# def computeArea(pos):
#     x, y = (zip(*pos))
#     return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

def sizeControl(blimp):
    
    baseline_diameter=1.64
    
    dia_ratio=2*blimp.radius/baseline_diameter
    
    fin_area=0.24*dia_ratio**2
    fin_tip=0.54*dia_ratio
    fin_root=0.91*dia_ratio
    
    control_area=0.08*dia_ratio
    control_tip=0.17*dia_ratio
    control_root=0.19*dia_ratio
    
    span=0.54*dia_ratio
    # mean=0.43*dia_ratio
    
    

# x=[0,-fin_tip,-fin_root*np.cos(np.radians(13)),0,-control_tip,-control_root*np.cos(np.radians(13))]
# y=[0,0,span-fin_root*np.sin(np.radians(13)),span,0,span-control_root*np.sin(np.radians(13))]

# plt.scatter(x,y)

# polygon = []
# polygon = plt.fill(x[0:4], y[0:4])
# area = computeArea(polygon[0].xy)

# polygon = []

# polygon = plt.fill([x[0],x[4],x[5],x[3]], [y[0],y[4],y[5],y[3]])
# area2 = computeArea(polygon[0].xy)

    # MAC=2/3*fin_root*(1+(fin_tip/fin_root)+(fin_tip/fin_root)**2)/(1+(fin_tip/fin_root))
    
    # naca=np.array([[1.0000,     0.00084],
    #                 [0.9500,     0.00537],
    #                 [0.9000,     0.00965],
    #                 [0.8000,     0.01749],
    #                 [0.7000,     0.02443],
    #                 [0.6000,     0.03043],
    #                 [0.5000,     0.03529],
    #                 [0.5000,     0.03529],
    #                 [0.4000,     0.03869],
    #                 [0.3000,     0.04001],
    #                 [0.2500,     0.03961],
    #                 [0.2000,     0.03825],
    #                 [0.1500,     0.03564],
    #                 [0.1000,     0.03121],
    #                 [0.0750,     0.02800],
    #                 [0.0500,     0.02369],
    #                 [0.0250,     0.01743],
    #                 [0.0125,     0.01263],
    #                 [0.0000,     0.00000],
    #                 [0.0125,     -0.01263],
    #                 [0.0250,     -0.01743],
    #                 [0.0500,     -0.02369],
    #                 [0.0750,     -0.02800],
    #                 [0.1000,     -0.03121],
    #                 [0.1500,     -0.03564],
    #                 [0.2000,     -0.03825],
    #                 [0.2500,     -0.03961],
    #                 [0.3000,     -0.04001],
    #                 [0.4000,     -0.03869],
    #                 [0.5000,     -0.03529],
    #                 [0.6000,     -0.03043],
    #                 [0.7000,     -0.02443],
    #                 [0.8000,     -0.01749],
    #                 [0.9000,     -0.00965],
    #                 [0.9500,     -0.00537],
    #                 [1.0000,     -0.00084]])
    
    # naca=naca.transpose()
    # naca=naca*MAC
    # # plt.scatter(naca[0],naca[1])
    
    # polygon = []
    # polygon = plt.fill(naca[0],naca[1])
    # area = computeArea(polygon[0].xy)
    # plt.close()
    # volume_correction_factor=0.82157407407
    # T=0.08
    # def func(x):
        # y=T/0.2*(0.2969*x**0.5+-0.126*x+-0.3516*x**2+0.2843*x**3+-0.1015*x**4)
        # return y
    # area=2*integrate.quad(func,0,1)[0]
    # def func2(x):
        # return area*(((fin_root-fin_tip)/span)*x+fin_tip)**2
    # volume=integrate.quad(func2,0,span)[0]*volume_correction_factor
    
    surface=2*span*fin_tip+span*fin_tip*1.116/2*0.736*1.0145 # first coeff: surface area calculation ratio, second: ratio vs trapezoid, third: ratio vs actual airfoil
    mass_fin=0.018*surface*(1-0.276)*1.26*2.36 # first: ratio of control surfaces, second, third:coefficients from book 
    mass_control=surface*0.276*0.3*4.88 #ratio, factor from book, conversion from lb/ft2 to kg/m2
    mass_actuator=surface*0.276*0.08*4.88*1.55 #ratio, factor from book, conversion, installation factor
    
    return sum([blimp.n_controls * mass_fin, blimp.n_controls * mass_control,  blimp.n_controls *mass_actuator]),surface,(fin_tip+fin_root)/2



