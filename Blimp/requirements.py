### VEHICLE REQUIREMENTS ###
max_MTOM            =        150     # [kg]  REQ-VEH-1
max_length          =        200     # [m]   REQ-VEH-2
max_radius          =         40     # [m]   REQ-VEH-2
n_sensors           =        100     # [-]   REQ-VEH-3
lifetime            =         10     # [yr]  REQ-VEH-4
explosive_potential =       6575 *10**6    # [J]  REQ-VEH-5

### STRUCTURAL REQUIREMENTS ###
gust_at_maxcruise       =         10.6          # [m/s]         REQ-VEH-STR-5
gust_at_typcruise       =          7.6          # [m/s]         REQ-VEH-STR-6
n_cycles                =       4000            # [-]           REQ-VEH-STR-7
load_factor_ult         =          2.1          # [-]           REQ-VEH-STR-11
load_factor_limit       =          1.4          # [-]           REQ-VEH-STR-12
sf_envelope             =          5            # [-]           REQ-VEH-STR-13
sf_susp_non_metal       =          2.25         # [-]           REQ-VEH-STR-13
sf_general              =          1.5          # [-]           REQ-VEH-STR-13
payload_mass            =         44            # [kg]          REQ-VEH-STR-15


### PROPULSION AND POWER ###
range_on_battery    =        100    # [km]  REQ-VEH-POW-2

### CONTROL AND OPERATIONS ###
range               =        350*10**3     # [m]  REQ-VEH-CO-12
path_accuracy       =         25     # [m]   REQ-VEH-CO-13
max_ground_alt      =        500     # [m]   REQ-VEH-CO-14
deployment_accuracy =         25     # [m]   REQ-VEH-CO-15
max_turn_radius     =        140     # [m]   REQ-VEH-CO-25
min_pitch_rate      =        0.6     # [deg/s] REQ-VEH-CO-26
min_yaw_rate        =        4.5     # [deg/s] REQ-VEH-CO-30


def checkRequirements(blimp):
    if blimp.radius > max_radius:
        print("Radius too big")
        return False
    elif blimp.length > max_length:
        print("Too long")
        return False
    # elif blimp.MTOM > max_MTOM:
    #     print("too heavy")
    #     return False
    elif blimp.explosive_potential > explosive_potential:
        print("Too explosive")
        return False
    else:
        print("within bounds")
        return True
