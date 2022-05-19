import unittest
import structures
from Archive import first_concept, propulsion_power
import projected_panel

class TestTest(unittest.TestCase):


    # def test_powercalc(self): #not able to test because idk how to handle the tmy variable
    #     self.assertEqual(propulsion_power.power_calc(5, 10, panel_angle, length_factor, tmy, elevation), (output 1, output 2))
    #     self.assertEqual(propulsion_power.power_calc(r, l, panel_angle, length_factor, tmy, elevation), (output 1, output 2))
    #     self.assertEqual(propulsion_power.power_calc(r, l, panel_angle, length_factor, tmy, elevation), (output 1, output 2))
    #     self.assertEqual(propulsion_power.power_calc(r, l, panel_angle, length_factor, tmy, elevation), (output 1, output 2))

    def test_required_density_gas(self):
        self.assertEqual(structures.required_density_gas((38.9, 45.9, 25), 0.6877249357326479)

    def test_volume_ballonets(self):
        self.assertEqual(structures.volume_ballonets(38.9, 0.6877),2.8078556911015298)
        self.assertEqual(structures.volume_ballonets(18.9, 0.2), 0.1580861105294994)
        self.assertEqual(structures.volume_ballonets(100, 0.9), 15.848866714676113)

    def test_pressure_blimp_gas(self):
        self.assertEqual(structures.pressure_blimp_gas(38.9, 2.807, 273.15), (273851.40163457964, 172526.40163457964))
        self.assertEqual(structures.pressure_blimp_gas(18.9, 2.307, 278.15), (273984.31759704056, 172659.31759704056))
        self.assertEqual(structures.pressure_blimp_gas(58.9, 1.807, 293.15), (298177.6885058233, 196852.68850582332))


    def test_stress_blimp(self):
        self.assertEqual(structures.stress_blimp(4.3, 172526, 0.003),1181.523)
        self.assertEqual(structures.stress_blimp(6.3,112526,0.0003), 123.64363333333331)
        self.assertEqual(structures.stress_blimp(0.3, 172526, 0.1), 0.25878899999999994)

    def test_surface_area(self):
        self.assertEqual(first_concept.surface_area(1, 4, 2, 2), 123.12478369553894)
        self.assertEqual(first_concept.surface_area(6, 2, 0.1, 10), 135.10735273715483)
        self.assertEqual(first_concept.surface_area(20, 1, 5, 2), 740.7766226741826)

    # def test_drag(self): #error (int object is not subscriptable), can be tested currently
    #     self.assertEqual(first_concept.drag((40, 0.5, 3, 1.255, 30), xxxx)

    def test_balloon_mass(self):
        self.assertEqual(first_concept.balloon_mass(40, 0.5, 4, 0.4, 0.2), ((150.71339323860903, 3.9148676411688634, 3.9148676411688634, 90.42803594316543)))
        self.assertEqual(first_concept.balloon_mass(80, 0.1, 3, 0.6, 0.1), ((620.2396414192259, 8.434326653017491, 1.6868653306034984, 434.16774899345813)))

    def test_solar(self):
        self.assertEqual(first_concept.solar(4, 2, 4, 0.5, 1, 5, 3), (226.27416997969522, 33.941125496954285))
        self.assertEqual(first_concept.solar(8, 0.5, 20, 0.1, 7, 3, 10), (475.17575695736, 197.98989873223334))

    # def test_velocity(self): #error formula, "max_eff" not defined, not able to test
    #     self.assertEqual(first_concept.velocity(1990, 0.8, 0.3, 19, 12), xxx)

    def test_surface_area(self):
        self.assertEqual(projected_panel.surface_area(5,3,6),271.32529661027246)
        self.assertEqual(projected_panel.surface_area(-1, -8, 10), (3959.6537055650356-3814.7493895463426j))



    def test_angle(self):
        self.assertEqual(projected_panel.angle(([3,2,1],[2,4,3]),0.624077252536407)








if __name__ = '__main__':
    unittest.main()