
# initial_volume_Hyd = 50.89 # m^3
# m_take_off = 58.078 # kg
# m_payload = 43.16 # kg

def required_density_gas(initial_volume_H,m_take_off,m_payload):
    """
    This definition calculates the required density of the gas 
    to lower the blimp (no payload,)
    no payload -> lowest buoyancy force to lower vehicle
    """

    density_air = 1.225 # kg/m^3
    
    final_density_gas = (density_air*initial_volume_H-(m_take_off-m_payload))/initial_volume_H
    return final_density_gas

#print(required_density_gas(initial_volume_Hyd,m_take_off,m_payload))
#density_gas_final = required_density_gas(initial_volume_Hyd,m_take_off,m_payload)

def volume_ballonets(initial_volume_H,final_density_gas):
    """
    This def calculates volume of the ballonets   
    to lower the vehicle              
    """
    density_H = 0.088 # kg/m^3
    mass_H = density_H*initial_volume_H
    density_air = 1.225 # kg/m^3

    # increment 
    volume_air_added = 1

    flag = 0
    while flag == 0:

        ### volume of hydrogen decreased by added volume of air
        new_volume_H = initial_volume_H - volume_air_added

        ### mass of hydrogen and air in blimp
        total_mass = mass_H + density_air*volume_air_added

        ### fractions of weight hydrogen/air to the total mass
        weight_air = density_air*volume_air_added/total_mass
        weight_H = mass_H/total_mass

        ### calculated density with added air
        new_density =  weight_H*(mass_H/(new_volume_H)) + weight_air*(density_air*volume_air_added/(initial_volume_H-(new_volume_H)))
        #print("new density", new_density) 

        ### check if density gas is reached
        # density of the gas is too low -> increase volume air to increase density gas
        if (final_density_gas-new_density)> 0.01:
            volume_air_added = volume_air_added +0.005*volume_air_added
            
        # density of the gas is too high -> decrease volume air to decrease density gas
        elif (final_density_gas-new_density)<-0.01:
            # lower added volume air
            volume_air_added = volume_air_added - +0.005*volume_air_added
            
        # the calculated density is close the desired density
        elif abs(final_density_gas-new_density)< 0.01:
            flag = 1
        

    return volume_air_added 

#print(volume_ballonets(initial_volume_Hyd,density_gas_final))
#new_volume_H = initial_volume_Hyd - volume_ballonets(initial_volume_Hyd,density_gas_final)

def pressure_blimp_gas(initial_volume_H,new_volume_H):
    """
    def returns the pressure (relative to surrounding pressure) 
    required to be carried by the envelope 
    """
    T = 273.15 # K
    R = 8.314  # JK^-1 mol^-1
    p_atm = 101325 # pa

    M_H = 1.00794*10**(-3) # kg/mol
    M_air = 28.97*10**(-3) #kg/mol

    density_H = 0.082 # kg/m^3
    density_air = 1.225 # kg/m^3

    m_H = density_H*initial_volume_H
    m_air = density_air*(initial_volume_H-new_volume_H)

    n_H = m_H/M_H
    n_air = m_air/M_air

    p_gas = ((n_H+n_air)*R*T)/initial_volume_H
    rel_p_gas = p_gas - p_atm

    return rel_p_gas

#print(pressure_blimp_gas(initial_volume_Hyd,new_volume_H))

#rel_p_gas = pressure_blimp_gas(initial_volume_Hyd,new_volume_H)
# Diameter_blimp = 6.3 #m
# wall_thickness = 0.0003 #m

def stress_blimp(diameter, inside_pressure, wall_thickness):
    """
    hoop stress for blimp
    """
        
    ss = inside_pressure*diameter/(2*wall_thickness)
    return ss*10**(-6)


initial_volume_Hyd = 50.89 # m^3
m_take_off = 58.078 # kg
m_payload = 43.16 # kg
Diameter_blimp = 2.36 #m
wall_thickness = 0.0006 #m

density_gas_final = required_density_gas(initial_volume_Hyd,m_take_off,m_payload)
new_volume_H = initial_volume_Hyd - volume_ballonets(initial_volume_Hyd,density_gas_final)
rel_p_gas = pressure_blimp_gas(initial_volume_Hyd,new_volume_H)
print(rel_p_gas)
hoop_stress = stress_blimp(Diameter_blimp,rel_p_gas,wall_thickness)
print(hoop_stress)
