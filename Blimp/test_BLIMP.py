import unittest
from Blimp.BLIMP import *

precision = 3

class TestTest(unittest.TestCase):
    def assertClose(self, a, b):
        self.assertEqual(round(a, precision), b)
        print(a)

    def test_sizeBalloon(self):
        testblimp = unpickle('Simon')
        testblimp.MTOM = 200
        testblimp.liftgas.spec_energy = 50
        testblimp.spheroid_ratio = 3
        testblimp.mass['payload'] = 50
        testblimp.balloon_thickness = 0.0005
        testblimp.material['envelope'].density = 0.5

        testblimp.sizeBalloon()

        print(testblimp.volume)
        print(testblimp.explosive_potential)
        print(testblimp.radius)
        print(testblimp.length)
        print(testblimp.radius_ballonet)
        print(testblimp.mass['ballonets'])
        print(testblimp.surface_area)
        print(testblimp.mass['envelope'])
        print(testblimp.ref_area)
        # self.volume = self.MTOM / lift_h2
        # self.explosive_potential = self.volume * self.liftgas.spec_energy
        # self.radius = ((3 * self.volume) / (4 * self.spheroid_ratio)) ** (1 / 3)
        # self.length = self.spheroid_ratio * self.radius * 2
        # self.balloon_thickness = struc.envelope_thickness(self, struc.envelope_pressure(self))
        #
        # ballonet_surface_frac = 1
        # self.radius_ballonet = (self.mass['payload'] / self.MTOM * self.volume * 3 / 8 / np.pi) ** (1 / 3)
        # self.mass['ballonets'] = 2 * 4 * np.pi * self.radius_ballonet ** 2 * ballonet_surface_frac * 0.176
        #
        # self.surface_area = 4 * np.pi * ((self.radius ** (2 * p) + 2 * (self.radius * self.length / 2) ** p) / 3) ** (
        #             1 / p)
        # # self.mass['envelope'] = self.surface_area * self.balloon_thickness * self.material['envelope'].density
        # self.mass['envelope'] = self.surface_area * 0.176
        # self.ref_area = self.volume ** (2 / 3)

    def test_sizeSolar(self):
        testblimp = unpickle('Simon')
        testblimp.area_solar = 33
        print('test')
        testblimp.sizeSolar()

        print(testblimp.power_solar)
        print(testblimp.mass['solar'])


        # self.panel_angle = self.panel_rows * self.solar_cell.width / self.radius
        # self.area_solar = 0.8 * 2 * self.length / 2 * self.radius * 2 * self.panel_angle
        #
        # shone_area = self.area_solar * irradiance_distribution(self, avg_sun_elevation)
        # net_power = shone_area * np.mean(tmy["DNI"]) + np.mean(tmy["DHI"]) * self.area_solar
        # self.power_solar = net_power * self.solar_cell.efficiency * self.solar_cell.fillfac
        # self.mass['solar'] = self.area_solar * self.solar_cell.density
        #
        # if np.isnan(self.power_solar):
        #     self.power_solar = 0

    def test_sizeBattery(self):
        testblimp = unpickle('Simon')
        testblimp.power_electronics = 77
        testblimp.CD = 0.06

        testblimp.sizeBattery()

        print(testblimp.battery_speed)
        print(testblimp.battery_capacity)
        print(testblimp.mass['battery'])
        print(testblimp.battery_charge)


if __name__ == '__main__':
    unittest.main()