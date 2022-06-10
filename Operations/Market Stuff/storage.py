
x_sensor = 0.085
y_sensor = 0.065
z_sensor = 0.0175

x_relay = 0.085
y_relay = 0.065
z_relay = 0.035

volume_sensors = x_sensor * y_sensor * z_sensor * 1.1 * 100000
volume_relays = x_relay * y_relay * z_relay * 1.1 * 70 * 2

x_pack_sensor = 1
y_pack_sensor = 1
z_pack_sensor = 1

print(volume_sensors)
