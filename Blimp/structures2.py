from BLIMP import Blimp
from Classes.gas import Gas, air
from Classes.materials import Material
import numpy as np


def envelope_pressure(blimp, mass_dropped, atm_gas=air):
    """
    Calculate the pressure inside the envelope due to ballonets
    :param blimp: [Blimp] Blimp object to be investigated [-]
    :param mass_dropped: [float] The mass dropped to be compensated by the ballonete subsystem [kg]
    :param atm_gas: [Gas] The atmospheric surrounding gas [-]
    :return: [float] Max. pressure difference between envelope and atmosphere [Pa]
    """
    m_final = blimp.MTOM - mass_dropped
    density_final = -m_final / blimp.volume + atm_gas.dens
    m_final_air = (density_final - blimp.liftgas.dens) * blimp.volume
    m_lifting_gas = blimp.liftgas.dens * blimp.volume
    mol_air = m_final_air / atm_gas.m_molar
    mol_lifting_gas = m_lifting_gas / blimp.liftgas.m_molar
    p_total = ((mol_air + mol_lifting_gas) * Gas.R * atm_gas.temp) / blimp.volume
    p_diff = p_total - atm_gas.pres
    return p_diff


def envelope_thickness(blimp, p_diff, max_radius, env_material, safety_factor = 5):
    """
    Through calculating critical von Mises stress for the envelope of the blimp,
    calculates the required material thickness.
    :param p_diff: [float] Max. pressure difference between the envelope [Pa]
    :param max_radius: [float] Max. local radius of the blimp envelope [m]
    :param env_material: [Material] Material used for the envelope [-]
    :return: [float] Thickness of material required for the envelope [m]
    """
    sigma_zz = 0  # Principal stress is 0 in z direction
    sigma_xx = (p_diff * max_radius) / 2  # Longit. stress. Assuming 1m thickness for now.
    sigma_yy = (p_diff * max_radius)  # Hoop stress. Assuming 1m thickness for now.
    sigma_vm = von_mises_stress(sigma_xx, sigma_yy, sigma_zz)  # Eq. von Mises stress
    t_req = sigma_vm / env_material.tensile_strength
    safe_t_req = t_req * safety_factor
    return safe_t_req

def von_mises_stress(sigma_a, sigma_b, sigma_c):
    """
    Calculate equivalent von Mises stress (relevant failure criterion for ductile materials)
    from the 3 principal stresses.
    :param sigma_a: [float] Principal stress [Pa]
    :param sigma_b: [float] Principal stress [Pa]
    :param sigma_c: [float] Principal stress [Pa]
    :return: [float] Equivalent von Mises stress [Pa]
    """
    return np.sqrt((((sigma_a - sigma_b) ** 2) + ((sigma_b - sigma_c) ** 2) + ((sigma_c - sigma_a) ** 2)) / 2)
