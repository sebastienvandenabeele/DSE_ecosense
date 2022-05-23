import numpy as np
import matplotlib.pyplot as plt

def computeArea(pos):
    x, y = (zip(*pos))
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

def sizeControl(blimp):
    
    naca_area=0.247495945409773
    
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
    
    volume=naca_area*span
    
    return volume, fin_area, fin_tip, fin_root, control_area, control_tip, control_root

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
#                [0.9500,     0.00537],
#                [0.9000,     0.00965],
#                [0.8000,     0.01749],
#                [0.7000,     0.02443],
#                [0.6000,     0.03043],
#                [0.5000,     0.03529],
#                [0.5000,     0.03529],
#                [0.4000,     0.03869],
#                [0.3000,     0.04001],
#                [0.2500,     0.03961],
#                [0.2000,     0.03825],
#                [0.1500,     0.03564],
#                [0.1000,     0.03121],
#                [0.0750,     0.02800],
#                [0.0500,     0.02369],
#                [0.0250,     0.01743],
#                [0.0125,     0.01263],
#                [0.0000,     0.00000],
#                [0.0125,     -0.01263],
#                [0.0250,     -0.01743],
#                [0.0500,     -0.02369],
#                [0.0750,     -0.02800],
#                [0.1000,     -0.03121],
#                [0.1500,     -0.03564],
#                [0.2000,     -0.03825],
#                [0.2500,     -0.03961],
#                [0.3000,     -0.04001],
#                [0.4000,     -0.03869],
#                [0.5000,     -0.03529],
#                [0.6000,     -0.03043],
#                [0.7000,     -0.02443],
#                [0.8000,     -0.01749],
#                [0.9000,     -0.00965],
#                [0.9500,     -0.00537],
#                [1.0000,     -0.00084]])

# naca=naca.transpose()
# naca=naca*MAC
# plt.scatter(naca[0],naca[1])

# polygon = []
# polygon = plt.fill(naca[0],naca[1])
# area = computeArea(polygon[0].xy)



