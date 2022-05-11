import numpy as np

# =============================================================================
# FUNCTIONS
# =============================================================================
def surface_area(a,b,c,p):
    return(4*np.pi*((((a*b)**p+(a*c)**p+(b*c)**p))/3)**(1/p))

def drag(vol,spheroid_ratio,dl_re,rho,V):
    A=vol**(2/3)
    dl=1/spheroid_ratio
    ld=spheroid_ratio   
    list_element=min(dl_re[:,0], key=lambda x:abs(x-dl))
    re=dl_re[np.where(dl_re[:,0]==list_element),1]
    CD=(0.172*ld**(1/3)+0.252*dl**1.2+1.032*dl**2.7)/((re*10**7)**(1/6))
    D=0.5*rho*V**2*A*CD
    return D
    
def balloon_mass(vol, spheroid_ratio,p,cover,foil):
    a=((3*vol)/(4*spheroid_ratio))**(1/3)
    b=a
    c=spheroid_ratio*a
    S=surface_area(a,b,c,p)
    m=S*(cover+foil)
    return S,a,2*c,m

def solar(irradiance,a,c,length_factor,ff,eff,solar_d):
    area=np.sqrt(2)*a*length_factor*ff*2*c
    power=eff*area*irradiance
    return power,(area*solar_d)

def velocity(power,prop_eff,motor_eff,D,v):
    T=(power*prop_eff*motor_eff)/(v/3.6)
    T_eff=(power*max_eff*prop_eff*motor_eff)/(v/3.6)
    diff=abs(D-T)
    diff_eff=abs(D-T_eff)
    v_max=v[np.where(diff[0]==min(diff[0]))]
    v_opt=v[np.where(diff_eff[0]==min(diff_eff[0]))]
    return v_max,v_opt[0]
    
# =============================================================================
# INPUTS
# =============================================================================
payload=25
box=3
propulsion=0.8
electronics=1
balloon=0
solar_cell=0
ballonette=0.75

# =============================================================================
# COEFFICIENTS
# =============================================================================
# Balloon calculations
spheroid_ratio=3
foil_t=0.000008
foil_d=11.36
linen_light_d=30
linen_heavy_d=150
silk_d=21.65
p=1.6075

# Drag calculation
dl_re=np.array([[0.05    ,2.36],
                [0.1     ,1.491],
                [0.15    ,1.138],
                [0.182   ,1],
                [0.2     ,0.94],
                [0.25    ,0.81],
                [0.3     ,0.716]
    ])
rho=1.225
v=np.arange(0,155,1)

# Propulsion
motor_eff=0.9
prop_eff=0.85
batt_c=4
batt_v=22.2
batt_e=batt_c*batt_v
max_eff=0.75
margin=1.1

#Solar
irradiance=350
eff=0.2
ff=0.8
length_factor=0.8
solar_d=0.42

#Helium
lift_he=1.0465
lift_h=1.14125

# =============================================================================
#  CALCULATION
# =============================================================================
for i in range(500):
    mass=payload+box+propulsion+electronics+balloon+solar_cell+ballonette
    vol=mass/lift_h
    S,a,c,balloon=balloon_mass(vol, spheroid_ratio, p, silk_d, foil_d)
    power,solar_cell=solar(irradiance, a, c, length_factor, ff, eff, solar_d)
    D=drag(vol, spheroid_ratio, dl_re, rho, v)
    v_max,v_opt=velocity(power/margin, prop_eff, motor_eff, D, v)