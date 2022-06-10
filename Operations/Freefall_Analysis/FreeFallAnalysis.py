from math import *
from matplotlib import pyplot as plt
from numpy import sign


class SensorObject:
    def __init__(self, x_init, y_init, gamma, m, vtot, cd_fall, A_fall, cd_wind, A_wind, v_wind):
        self.x, self.y = x_init, y_init  # [m]
        self.gamma = gamma  # [rad]
        self.vtot = vtot
        self.v_wind = v_wind

        self.cd_fall = cd_fall  # [-]
        self.cd_wind = cd_wind  # [-]
        self.m = m  # [kg]
        self.A_fall = A_fall  # [m^2]
        self.A_wind = A_wind  # [m^2]

        self.g = 9.80665  # [m/s^2]
        self.rho = 1.225  # [kg/m^3]

        self.dt = 0.01  # [s]

        self.vx, self.vy = vtot * cos(self.gamma), vtot * sin(self.gamma)
        self.Fx, self.Fy = 0, 0
        self.ax, self.ay = 0, 0

        self.xlst, self.ylst = [self.x], [self.y]

        done = False
        self.t = 0

        while self.y > 15:
            self.t = self.t + self.dt
            self.calculate_forces()
            self.calculate_acceleration()
            self.update_velocities()
            self.update_location()

    def calculate_forces(self):
        Fgrav = self.g * self.m
        Fdrag = self.cd_fall * 0.5 * self.rho * self.vtot**2 * self.A_fall
        Fwind = sign(self.v_wind) * self.cd_wind * 0.5 * self.rho * self.v_wind**2 * self.A_wind

        self.Fx = - Fdrag * cos(self.gamma) + Fwind
        self.Fy = -Fgrav + (Fdrag * sin(self.gamma))

    def calculate_acceleration(self):
        self.ax = self.Fx / self.m
        self.ay = self.Fy / self.m

    def update_velocities(self):
        self.vx = self.vx + self.ax * self.dt
        self.vy = self.vy + self.ay * self.dt
        self.gamma = abs(atan2(self.vy, self.vx))
        self.vtot = sqrt(self.vx**2 + self.vy**2)

    def update_location(self):
        self.x = self.x + self.vx * self.dt
        self.y = self.y + self.vy * self.dt

        self.xlst.append(self.x)
        self.ylst.append(self.y)

    def return_positions(self):
        return self.xlst, self.ylst

    def return_deploytime(self):
        return self.t

x_init, y_init = 0, 310  # [m]
vtot = 15 # [m/s]
gamma = 0  # [rad]
cd_fall = 0.9  # [-]
m = 0.08  # [kg]
A_fall = 0.0012025  # [m^2]

v_wind = 4.17  # [m/s]
cd_wind = 1.15  # [-]
A_wind = 0.005525  # [m^2]

sensorfall_nowind = SensorObject(x_init, y_init, gamma, m, vtot, cd_fall, A_fall, 0, 0, 0)
xlst_nowind, ylst_nowind = sensorfall_nowind.return_positions()

sensorfall_maxwind = SensorObject(x_init, y_init, gamma, m, vtot, cd_fall, A_fall, cd_wind, A_wind, v_wind)
xlst_maxwind, ylst_maxwind = sensorfall_maxwind.return_positions()

sensorfall_minwind = SensorObject(x_init, y_init, gamma, m, vtot, cd_fall, A_fall, cd_wind, A_wind, -v_wind)
xlst_minwind, ylst_minwind = sensorfall_minwind.return_positions()

deploytime = round((sensorfall_minwind.return_deploytime() + sensorfall_nowind.return_deploytime() +
              sensorfall_maxwind.return_deploytime()) / 3, 2)

print(sensorfall_maxwind.return_deploytime(), sensorfall_nowind.return_deploytime(), sensorfall_minwind.return_deploytime())
plt.plot(xlst_nowind, ylst_nowind, label="No WInd")
plt.plot(xlst_maxwind, ylst_maxwind, label="Max WInd")
plt.plot(xlst_minwind, ylst_minwind, label="Min WInd")

acc1 = round(xlst_maxwind[-1] - xlst_nowind[-1])
acc2 = round(xlst_nowind[-1] - xlst_minwind[-1])

plt.legend()
plt.title(f"Accuracy of deployment is {(acc1 + acc2)/2} m. Time until string deployment is {deploytime} s")
plt.show()