mass_H = 3.17 #kg
initial_volume_H = 38.9 # m^3
density_air = 1.225 # kg/m^3
final_density_gas = 0.69 # kg/m^3
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
    #print("fraction air", weight_air)
    #print("fraction H", weight_H)


    ### calculated density with added air
    new_density =  weight_H*(mass_H/(new_volume_H)) + weight_air*(density_air*volume_air_added/(initial_volume_H-(new_volume_H)))
    #print("new density", new_density) 


    ### check if density gas is reached

    # density of the gas is too low -> increase volume air to increase density gas
    if (final_density_gas-new_density)> 0.01:
        volume_air_added = volume_air_added +0.005*volume_air_added
        
    # density of the gas is too hihg -> decrease volume air to decrease density gas
    elif (final_density_gas-new_density)<-0.01:
        # lower added volume air
        volume_air_added = volume_air_added - +0.005*volume_air_added
        
    # the calculated density is close the desired density
    elif abs(final_density_gas-new_density)< 0.01:
        print(new_density)
        print(new_volume_H)
        flag = 1
        
        
