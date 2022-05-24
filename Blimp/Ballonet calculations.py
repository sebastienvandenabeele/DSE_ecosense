from math import *


Dp = 25e3 # [Pa] Pressure difference
Vol_env = 100 # [m^3] Volume of envelope
Vol_bt = Vol_env*0.1 # [m^3] Ballonet volume
r_inlet = 0.05 # [m] Inlet radius
r_outlet = 0.1 # [m] Outlet radius
A_inlet = pi*r_inlet**2 # [m^2] Inlet Area
A_outlet = pi*r_outlet**2 # [m^2] Outlet Area
rho_air = 1.225 # [kg/m^3] Air density


inflation_time = 180 # [s] 
mass_flow_outlet = Vol_bt/inflation_time # [m^3/s]

V_outlet = mass_flow_outlet/A_outlet # [m/s] Outlet velocity

mass_flow_inlet = A_inlet*(2/rho_air*(Dp + rho_air*(V_outlet**2)/2))**0.5



print('Airflow required:', mass_flow_inlet, 'm^3/s')
print('Airflow required:', mass_flow_inlet*3600, 'm^3/h')
