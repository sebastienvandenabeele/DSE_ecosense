from re import L
import numpy as np
import unittest
import simulation_functions as simfunc


class simulation_unit_tests(unittest.TestCase):
    # Cone parameters were skipped because the calculations are the same as the first two steps of ellipse parameters
    # Skipped Triangle points for now, probably better to verify it using the GUI
    # Centre caluclations will be verified using the GUI
    # Relevant points were checked visually
    # the first part of get_concentration was verified by plotting the mesh, the relevant points and their coordinates in both the global and local smoke coordinate system

    def test_mc(self):
        # Set dummy parameters
        rh = np.array([0, 0, 10, 32, 64, 10000])
        t = np.array([0, 20, 25, 40, 100, 50000])

        # Check resulting values against hand calulated values (mention level of accuracy in report)
        np.testing.assert_array_almost_equal(simfunc.MC(
            rh, t), np.array([np.nan, 3.810387381, 3.941729227, 4.25377195, 3.080697696, 6008.878727]))

    def test_ffdi(self):
        # Set dummy parameters
        mc = np.array([0, 3, 6, 20, 30, 50])
        u = np.array([0, 5, 10, 30, 50, 100])

        # Check resulting values against hand calulated values (mention level of accuracy in report)
        np.testing.assert_array_almost_equal(simfunc.FFDI(
            mc, u), np.array([np.inf, 37.80609687, 9.913141521, 1.263036085, 0.860743858, 0.948672042]))

    def test_r(self):
        # Set dummy parameters
        ffdi = np.array([0, 5, 10, 50, 100, 10000])
        w = 23.57

        # Check resulting values against hand calulated values (mention level of accuracy in report)
        np.testing.assert_array_almost_equal(simfunc.R(
            ffdi, w), np.array([0, 0.14142, 0.28284, 1.4142, 2.8284, 282.84]))

    def test_read_and_edit_samples(self):
        # Load dummy samples CSV
        df = simfunc.read_and_edit_samples("./testing_data/dummy_samples.csv")

        # Verify that everything is calculated properly
        np.testing.assert_array_almost_equal(
            df["MC"].values, simfunc.MC(df["RH"].values, df["temp"].values))
        np.testing.assert_array_almost_equal(
            df["FFDI"].values, simfunc.FFDI(df["MC"].values, df["wind_spd"].values))
        np.testing.assert_array_almost_equal(
            df["R"],  simfunc.R(df["FFDI"].values, 23.57)/3.6)
        np.testing.assert_array_almost_equal(
            df["LB"], 1+10*(1-np.exp(-0.06*(1/3.6)*df["wind_spd"].values)))

        # Print the dataframe to check whether the samples have been filtered properly
        print(df)

    def test_ellipse_parameters(self):
        # Set dummy parameters
        lb = np.array([0.5, 1.5, 4, 8, 20, 100])
        t = np.array([5, 20, 25, 40, 100, 50000])
        R = np.array([0.5, 1, 5, 10, 50, 500])

        # Check resulting values against hand calulated values (mention level of accuracy in report)
        np.testing.assert_array_almost_equal(simfunc.ellips_params(
            t, R, lb), np.array([[2.5, 20, 125, 400, 5000, 25000000], [2.272727273, 13.33333333, 31.25, 50, 250, 250000], [0.520747238, 7.453559925, 60.51536478, 198.4313483, 2496.873044, 12499374.98]]), decimal=2)

    def test_initial_gas_distribution(self):
        # Set dummy parameters
        gases = ["CO", "H2"]
        time = [0, 30, 60, 93, 420, 720]

        # Run function for all combinations
        concentrations = []
        for gas in gases:
            for t in time:
                concentrations.append(np.float(
                    simfunc.initial_gas_concentration(gas, t)))

        # Run test
        np.testing.assert_array_almost_equal(
            concentrations, np.array([0, 0.425, 0.85, 2.885, 23.3, 42.7, 0, 0.15, 0.3, 0.355, 0.5, 4]))


    def test_get_concentration(self):
        centre = np.array([0, 0])
        wind_dir = 0
        t_max = 10*60
        N = int(100*(t_max/(8*60)))
        gas = "CO"
        lb = 1.5
        time = np.linspace(0, t_max, N)
        width_triangle = np.linspace(0, 200, N)
        length_triangle = width_triangle * lb
        xy = np.array([0, width_triangle[-1]/3])
        gas_init_ppm = simfunc.initial_gas_concentration(gas, time)
        concentration = simfunc.get_concentration(
            xy, centre, wind_dir, N-1, width_triangle, length_triangle, time, gas_init_ppm)
        np.testing.assert_almost_equal(concentration, 0.0228638894)

if __name__ == '__main__':
    unittest.main()
