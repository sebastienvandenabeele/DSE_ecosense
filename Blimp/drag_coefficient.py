import numpy as np
def calculateCD(Shlimp,rho):
    mu=18.18*10**(-7)
    
    #body
    Re=rho*Shlimp.cruiseV/3.6*Shlimp.length/mu
    Cf_body=0.455/((np.log10(Re))**2.58)
    FF_body = 1+1.5/Shlimp.spheroid_ratio**1.5+7/Shlimp.spheroid_ratio**3
    S=Shlimp.surface_area
    V=Shlimp.volume
    
    Cd0_body=0.5*FF_body*Cf_body*S/(V**(2/3))
    # print('Body: ',Cd0_body)
    
    #tail
    FF_tail=1+1.2*0.08+100*0.08**4
    Re_tail=rho*Shlimp.cruiseV/3.6*Shlimp.control_chord/mu
    S_tail= Shlimp.n_fins * Shlimp.control_surface
    Cf_tail=0.455/(np.log10(Re_tail)**2.58)
    
    Cd0_tail=FF_tail*Cf_tail*S_tail/(V**(2/3))
    # print('Tail: ',Cd0_tail)
    
    #cabin+gondolla
    # Cd0_gond=(0.108*Cd0_body*V**(2/3)+7.7)/V**(2/3)
    Cd0_gond=0.00256
    # print('Gondolla: ',Cd0_gond)
    
    #engine nacelle drag
    # Cd0_nacelle=Shlimp.n_engines*4.25/V**(2/3)
    Cd0_nacelle=0.00085
    # print('Nacelle: ',Cd0_nacelle)
    
    #engine mount
    # Cd0_mount=(0.044*Cd0_body*V**(2/3)+0.92)/V**(2/3)
    Cd0_mount=0.00122
    # print('Mount: ',Cd0_mount)
    
    #cables
    # Cd0_cables=(9.7*10**(-6)*V+10.22)/V**(2/3)
    Cd0_cables=0.00199
    # print('Cables: ',Cd0_cables)
    
    #landing gear
    # Cd0_lg=(1.76*10**(-6)*V+0.92)/V**(2/3)
    Cd0_lg=0.00027
    # print('LG: ',Cd0_lg)
    
    #interference
    Cd0_int=(4.78*10**(-6)*V)/V**(2/3)
    # print('Interference: ',Cd0_int)
    
    Cd0=Cd0_body+Cd0_tail+Cd0_gond+Cd0_nacelle+Cd0_mount+Cd0_cables+Cd0_lg+Cd0_int
    # print(Cd0)
    
    return Cd0