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
network = sensors + relays + sensor_manufacturing + \
    relay_manufacturing + ground_station


# Vehicle Costs
no_use = 1000
solar_panels = 5962.68
hydrogen = 85.6
electronics = 7132.01
engines = 552
envelope = 4000
deployment = 7000
fins = 700
gondola = 5000
manufacturing = 10000
vehicle = (solar_panels + hydrogen + electronics +
           engines + envelope + deployment + fins + manufacturing + gondola)/no_use * 2

# Operations Costs
drone_pilot = 3 * (8+2) * 180
technicians = 3 * (8+2) * 40
national_park_flying_permit = 2 * 2000
motorhome = 2500
living_expenses = 100 * 4 * 2
ford_ranger_rental = 1400  # for three days with trailer
fuel = 100  # 80 liters
operations = drone_pilot + technicians + \
    national_park_flying_permit + motorhome + \
    living_expenses + ford_ranger_rental + fuel

# Recurring Costs
software_engineer = 50000/8 * 5  # one can handle 8 missions
server = 4000 * 5  # one per mission
# gross estimate at 25% of blimp cost per year
maintenance = 500
recurring = software_engineer + server + maintenance

# Misc
hydrogen_delivery = 40
freight = 33.75
energy = 60
salaries = 31250
office = 3750
misc = freight + hydrogen_delivery + energy + salaries + office

final_cost_keur_arr = np.array(
    [network, vehicle, operations, recurring, misc])/1000

print(final_cost_keur_arr*1000)
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
