import numpy as np
import scipy.optimize as sco
import pandas as pd
import os


def get_link_margin_node_relay(d):
    p_transmitter = 20  # dBm
    g_transmitter = 3  # dBi
    g_receiver = 3  # dBi
    cable_loss = 1  # dBm
    f = 1020  # MHz
    h_transmitter = 1  # m
    h_receiver = 30  # m
    bandwidth = 62500  # Hz
    sensitivity = -174 + 10 * np.log10(bandwidth) + 6 - 20
    path_loss = 0.48 * f**0.43 * d**0.13 + 40 * \
        np.log10(d) - 20*np.log10(h_transmitter) - 20*np.log10(h_receiver)
    return p_transmitter + g_transmitter + g_receiver - cable_loss*2 - path_loss - sensitivity - 3


def get_link_margin_relay_relay(d):
    p_transmitter = 20  # dBm
    g_transmitter = 3  # dBi
    g_receiver = 3  # dBi
    cable_loss = 1  # dBm
    f = 1020  # MHz
    h_transmitter = 20  # m
    h_receiver = 20  # m
    bandwidth = 62500  # Hz
    sensitivity = -174 + 10 * np.log10(bandwidth) + 6 - 20
    path_loss = 0.48 * f**0.43 * d**0.13 + 40 * \
        np.log10(d) - 20*np.log10(h_transmitter) - 20*np.log10(h_receiver)
    print(path_loss)
    return p_transmitter + g_transmitter + g_receiver - cable_loss*2 - path_loss - sensitivity - 3


result_node_relay = sco.root_scalar(
    get_link_margin_node_relay, method='bisect', bracket=[5000, 100000])

result_relay_relay = sco.root_scalar(
    get_link_margin_relay_relay, method='bisect', bracket=[5000, 100000000])

print(result_relay_relay)
# df_test = pd.DataFrame(index=range(12), columns=[
#                        "Status", "Temp", "Hum", "Fire", "CO", "Gas", "Disturb"])

# req_list = []

# for i in range(10000):
#     df_test["Status"] = np.ones(12, dtype=int)
#     df_test["Temp"] = np.round(np.random.uniform(10.000, 40.000, 12), 2)
#     df_test["Hum"] = np.round(np.random.uniform(0.000, 100.000, 12), 2)
#     df_test["Fire"] = np.ones(12, dtype=int)
#     df_test["Disturb"] = np.ones(12, dtype=int)
#     df_test["CO"] = np.round(np.random.uniform(0.000, 100.000, 12), 2)
#     df_test["Gas"] = np.round(np.random.uniform(0.000, 100.000, 12), 2)
#     df_test.to_csv("bitrate_test.csv", index=False)

#     req_bps = (os.path.getsize("bitrate_test.csv") + 4) * 8
#     req_list.append(req_bps)

# req_array = np.array(req_list)
# print(req_array.max())

df_test_2 = pd.DataFrame(index=range(3), columns=[
                         "Temp", "Hum", "CO", "Gas", "Disturb"])

req_list = []

for i in range(10000):
    df_test_2["Temp"] = np.round(np.random.uniform(10.000, 40.000, 3), 2)
    df_test_2["Hum"] = np.round(np.random.uniform(0.000, 100.000, 3), 2)
    df_test_2["CO"] = np.round(np.random.uniform(0.000, 100.000, 3), 2)
    df_test_2["Gas"] = np.round(np.random.uniform(0.000, 100.000, 3), 2)
    df_test_2.to_csv("bitrate_test_2.csv", index=False)

    req_bps = (os.path.getsize("bitrate_test_2.csv") + 4 + 4*1089) * 8
    req_list.append(req_bps)

req_array = np.array(req_list)
print(req_array.max())
