import numpy as np
from matplotlib import pyplot as plt
from BLIMP import *

total_PL_weight = 84.85  # [kg]
deployment_range = 300  # [km]
trip_range = 200  # [km]
sun_time = 5 * 3600


for n in range(2, 10):
    range = (trip_range + deployment_range / n) * 1000
    min_velocity = range / sun_time

    payload_mass = total_PL_weight / n

    blimp = Blimp(name=str('Blimp' + str(n) + 'flights'),
                  balloon_pressure=500,
                  mass_payload=payload_mass,
                  mass_deployment=15,
                  n_fins=4,
                  n_engines=3,
                  envelope_material=mat.polyethylene_fiber,
                  target_speed=min_velocity,
                  electronics=el.config_option_1,
                  engine=eng.tmt_4130_300,
                  length_factor=0.9,
                  spheroid_ratio= 3,
                  liftgas=gas.hydrogen,
                  solar_cell= solar.maxeon_gen3)
    print('Number of flights: ', n)
    blimp.report()
    blimp.estimateCost()
    blimp.save()
