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

df_tmy, meta_dict = pvlib.iotools.read_tmy3("C:/Users/tilen/Downloads/tmy.csv")
df_tmy = df_tmy.reset_index()
for i in range(len(df_tmy)):
    df_tmy["Time (HH:MM)"][i]=int(df_tmy["Time (HH:MM)"][i].split(":")[0])
df_tmy["Time (HH:MM)"]=df_tmy["Time (HH:MM)"]+10
df_tmy=df_tmy[df_tmy["Time (HH:MM)"] >= 11]
df_tmy=df_tmy[df_tmy["Time (HH:MM)"] <= 15]
df_tmy = df_tmy.reset_index()
df_tmy.drop(df_tmy.index[400:1300], axis=0, inplace=True)

# print(np.mean(df_tmy["GHI"]))
# print(np.mean(df_tmy["DNI"]))
# print(np.mean(df_tmy["DHI"]))

# plt.plot(df_tmy["GHI"])
# plt.plot(df_tmy["DNI"])
# plt.plot(df_tmy["DHI"])

dni=584.5015783783784 # gotten from previous code
dhi=200.45297297297273
angle=np.radians(52)
d=2*2.158685380431896
L=2*6.476056141295688

Ap=(np.pi*d)/4*(np.sqrt(np.cos(angle)**2+((L/d)**2)*np.sin(angle)**2))

panel_area=20
blimp_area=140
panel_ratio=panel_area/(0.5*blimp_area) # solar panel area/ 0.5 blimp area

A=panel_ratio*Ap

power_max=A*np.mean(df_tmy["DNI"])+np.mean(df_tmy["DHI"])*panel_area

