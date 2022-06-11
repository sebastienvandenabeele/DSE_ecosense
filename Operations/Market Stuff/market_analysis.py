import matplotlib.pyplot as plt
import numpy as np

# Everything is done for a single 10x10km area containing 1089 sensors and 7 relays deployed in 2 trips (mission lasts 5 years)
flights_per_year = 24 * 2

# Network Costs
sensors = 1089 * 45.5
relays = 7 * 32.03
sensor_manufacturing = 2950
relay_manufacturing = 196
ground_station = 550  # From Dryad
misc = 1000
network = sensors + relays + sensor_manufacturing + \
    relay_manufacturing + ground_station + misc


# Vehicle Costs
no_use = 1000
solar_panels = 6683.05
hydrogen = 71.61
electronics = 6179.78
engines = 548.16
envelope = 2740.29
deployment = 1000
fins = 520
manufacturing = 100000
misc = 10000
vehicle = (solar_panels + hydrogen + electronics +
           engines + envelope + deployment + fins + manufacturing + misc)/no_use * 2

# Operations Costs
drone_pilot = 3 * (8+2) * 180
technicians = 3 * (8+2) * 40
national_park_flying_permit = 2 * 2000
motorhome = 2 * 2500
living_expenses = 100 * 4 * 2
ford_ranger_rental = 1000  # for three days with trailer
fuel = 100  # 80 liters
operations = drone_pilot + technicians + \
    national_park_flying_permit + motorhome + \
    living_expenses + ford_ranger_rental + fuel

# Recurring Costs
software_engineer = 50000/8 * 5  # one can handle 8 missions
server = 4000 * 5  # one per mission
# gross estimate at 25% of blimp cost per year
maintenance = 0.25 * vehicle / flights_per_year
recurring = software_engineer + server + maintenance

# Misc
hydorgen_delivery = 1000
freight = 0.03 * 4350 * 0.250
energy = 50
salaries = 2500 * 5 * 5 * 12 / flights_per_year * 2
office = 1500 * 12 * 5 / flights_per_year * 2
misc = freight + hydorgen_delivery + energy + salaries + office

final_cost_keur_arr = np.array(
    [network, vehicle, operations, recurring, misc])/1000
final_cost_keur = np.round(np.sum(final_cost_keur_arr), 2)

# Profit Margin
# costs of 5k per km2 every 5 years (assuming fire cycle of 5 years, 62% accuracy, 79% of forest burns per 5 years)
sale_price = 450 * 5 * 100 * 0.75  # Added 25% tax
sale_cost = final_cost_keur * 1000
profit_margin = np.round((sale_price - sale_cost)/sale_price * 100, 2)
profit_per_year = profit_margin/100 * sale_price * flights_per_year/12 / 1000
print(f"Profit Margin: {profit_margin}%")
print(f"Total: EUR {final_cost_keur}k")
print(f"Yearly Profits: EUR {profit_per_year}k")

cost_labels = ['Sensor Network', 'Deployment Vehicle',
               'Deployment Costs', 'Recurring Costs']
colors = ['tab:blue', 'tab:red', 'tab:gray', 'tab:orange']
pie = plt.pie(final_cost_keur_arr, autopct='%1.1f%%', colors=colors)
plt.legend(pie[0], cost_labels, bbox_to_anchor=(1, 0.5), loc="upper right", fontsize=10,
           bbox_transform=plt.gcf().transFigure)
plt.title(f'Cost Breakdown')
plt.axis('equal')
# plt.show()
