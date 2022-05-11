# =============================================================================
# propulsion mass
# velocity
# power
# design
# =============================================================================

# =============================================================================
# VECTORING:
    # 4 to 6% of the propulsion system or 0.12 to 0.16 kg per kg of vectored mass
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt
import pvlib

def read_irradiance():
    df_tmy, meta_dict = pvlib.iotools.read_tmy3("tmy.csv")
    df_tmy = df_tmy.reset_index()
    for i in range(len(df_tmy)):
        df_tmy["Time (HH:MM)"][i]=int(df_tmy["Time (HH:MM)"][i].split(":")[0])
    df_tmy["Time (HH:MM)"]=df_tmy["Time (HH:MM)"]+10
    df_tmy=df_tmy[df_tmy["Time (HH:MM)"] >= 11]
    df_tmy=df_tmy[df_tmy["Time (HH:MM)"] <= 16]
    df_tmy = df_tmy.reset_index()
    df_tmy.drop(df_tmy.index[400:1300], axis=0, inplace=True)
    return df_tmy
    
    # print(np.mean(df_tmy["GHI"]))
    # print(np.mean(df_tmy["DNI"]))
    # print(np.mean(df_tmy["DHI"]))
    
    # plt.plot(df_tmy["GHI"])
    # plt.plot(df_tmy["DNI"])
    # plt.plot(df_tmy["DHI"])
    
    #dni=np.mean(df_tmy["DNI"])
    #dhi=np.mean(df_tmy["DHI"])
    #
    #d=2*a
    #L=2*c
    
    # =============================================================================
    # Ap=(np.pi*d)/4*(np.sqrt(np.cos(angle)**2+((L/d)**2)*np.sin(angle)**2))
    # 
    # panel_area=10
    # blimp_area=140
    # panel_ratio=panel_area/(0.5*blimp_area) # solar panel area/ 0.5 blimp area
    # 
    # A=panel_ratio*Ap
    # =============================================================================
def power_calc(a, c, panel_angle, length_factor,tmy):
    angle = np.radians(52)
    panel_angle=np.radians(panel_angle)
    panel_area=0.8*2*c*a*2*panel_angle
    a_min= 2*np.sin(panel_angle)*a*length_factor*2*c*np.cos(angle)
    a_max= (1-np.cos(angle+panel_angle))*a*0.8*2*c
    
    power_max=a_min*np.mean(tmy["DNI"])+np.mean(tmy["DHI"])*panel_area
    
    efficiency=0.8*0.2
    
    power_actual=power_max*efficiency
    return power_actual, panel_area
