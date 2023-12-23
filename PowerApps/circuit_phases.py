import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Any

def create_phase_dict(name, id, ph, ground_point, cartesian1, R, X, polar2, line2neutral_kv,
                    line2neutral_deg, current_mag_ka, current_ang_deg):
    """
    Create a phase dictionary with specific parameters.

    Args:
    - name (str): Name of the phase.
    - id (int): Identifier of the phase.
    - ph (str): Phase details.
    - ground_point (tuple): Coordinates of the ground point.
    - cartesian1 (tuple): Coordinates of the point.
    - R (float): Resistance value.
    - X (float): Reactance value.
    - polar2 (float): [Description of polar2]
    - line2neutral_kv (float): Line to neutral kilovolts.
    - line2neutral_deg (float): Line to neutral degrees.

    Returns:
    - dict: A dictionary containing phase information.
    """
    return {
        'name': name,
        'id': id,
        'ph': ph,
        'ground_point': ground_point,
        'cartesian1': cartesian1,
        'R': R,
        'X': X,
        'polar2': polar2,
        'line2neutral_kv': line2neutral_kv,
        'line2neutral_deg': line2neutral_deg,
        'current_mag_ka': current_mag_ka,
        'current_ang_deg': current_ang_deg
    }




def create_phases(circuit_type: int, dataFrame: pd.DataFrame, phases_c1: List[float], phases_c2: List[float]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Generates phase dictionaries based on circuit type and DataFrame information.

    Args:
    - circuit_type (int): Type of circuit.
    - dataFrame (pd.DataFrame): DataFrame containing tower ground impedance data.
    - phases_c1 (List[float]): List of phase angles for circuit type 1.
    - phases_c2 (List[float]): List of phase angles for circuit type 2.

    Returns:
    - Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]: Tuple containing energization info for LT and DT.
    """
    ground_point_LT = 1
    ground_point_DT = 2
    cartesian1 = 1
    polar2 = 2
    r_sw = 0  
    x_sw = 0 
    if circuit_type ==1:

        # Get values
        r_abc_term1 = 0  
        x_abc_term1 = 0  
        line2neutral_kv = dataFrame.iloc[0]['crddb_linevoltage'] / np.sqrt(3)  # pu
        line2neutral_deg = phases_c1

        # Create phase dictionaries
        c1_phase_a_term1 = create_phase_dict('a', 1, 1, ground_point_LT, cartesian1, r_abc_term1, x_abc_term1, polar2,
                                        line2neutral_kv, line2neutral_deg[0], 0, 0)
        c1_phase_b_term1 = create_phase_dict('b', 2, 2, ground_point_LT, cartesian1, r_abc_term1, x_abc_term1, polar2,
                                        line2neutral_kv, line2neutral_deg[1], 0, 0)
        c1_phase_c_term1 = create_phase_dict('c', 3, 3, ground_point_LT, cartesian1, r_abc_term1, x_abc_term1, polar2,
                                        line2neutral_kv, line2neutral_deg[2], 0, 0)
        phase_pipe_term1 = create_phase_dict('pipe', 5, 5, ground_point_DT, cartesian1, 0, 0, 0, 0, 0, 0, 0)
        
        sw_ = create_phase_dict('sw', 4, 4, ground_point_LT, cartesian1, r_sw, x_sw, polar2, 0, 0,  0, 0)

            # Get values (assuming r_pipe and x_pipe are already defined)
        r_abc_term2 = (dataFrame.iloc[0]['crddb_linevoltage'] * 1e3 / np.sqrt(3)) / dataFrame.iloc[0]["crddb_steadystatecurrent"]
        x_abc_term2 = 0

        line2neutral_kv = 0
        line2neutral_deg = 0

        current_mag_ka = dataFrame.iloc[0]["crddb_contributionfaultcurrent_term2_mod"]
        current_ang_deg = dataFrame.iloc[0]["crddb_contributionfaultcurrent_term2_phase"]

        # Create phase dictionaries using the create_phase_dict function
        c1_phase_a_term2 = create_phase_dict('a', 1, 1, ground_point_LT, cartesian1, r_abc_term2, x_abc_term2, polar2, 
                                        line2neutral_kv, line2neutral_deg, current_mag_ka, current_ang_deg)

        c1_phase_b_term2 = create_phase_dict('b', 2, 2, ground_point_LT, cartesian1, r_abc_term2, x_abc_term2, polar2,
                                        line2neutral_kv, line2neutral_deg, current_mag_ka, current_ang_deg)

        c1_phase_c_term2 = create_phase_dict('c', 3, 3, ground_point_LT, cartesian1, r_abc_term2, x_abc_term2, polar2, 
                                        line2neutral_kv, line2neutral_deg, current_mag_ka, current_ang_deg)

        phase_pipe_term2 = create_phase_dict('pipe', 5, 5, ground_point_DT, cartesian1, 0, 0, polar2, 0, 0, 0, 0)

        
        energization_info_lt = [c1_phase_a_term1, c1_phase_b_term1, c1_phase_c_term1, sw_, phase_pipe_term1]
        energization_info_dt = [c1_phase_a_term2, c1_phase_b_term2, c1_phase_c_term2, sw_, phase_pipe_term2]
        return energization_info_lt, energization_info_dt

    elif circuit_type == 2:

        # Get values
        r_abc_term1 = 0  
        x_abc_term1 = 0  
        line2neutral_kv = dataFrame.iloc[0]['crddb_linevoltage'] / np.sqrt(3)  # pu
        line2neutral_deg = phases_c1

        # Create phase dictionaries
        c1_phase_a_term1 = create_phase_dict('a', 1, 1, ground_point_LT, cartesian1, r_abc_term1, x_abc_term1, polar2,
                                        line2neutral_kv, line2neutral_deg[0], 0, 0)
        c1_phase_b_term1 = create_phase_dict('b', 2, 2, ground_point_LT, cartesian1, r_abc_term1, x_abc_term1, polar2,
                                        line2neutral_kv, line2neutral_deg[1], 0, 0)
        c1_phase_c_term1 = create_phase_dict('c', 3, 3, ground_point_LT, cartesian1, r_abc_term1, x_abc_term1, polar2,
                                        line2neutral_kv, line2neutral_deg[2], 0, 0)
        phase_pipe_term1 = create_phase_dict('pipe', 8, 8, ground_point_DT, cartesian1, 0, 0, 0, 0, 0, 0, 0)
        
        sw_ = create_phase_dict('sw', 7, 7, ground_point_LT, cartesian1, r_sw, x_sw, polar2, 0, 0,  0, 0)

            # Get values (assuming r_pipe and x_pipe are already defined)
        r_abc_term2 = (dataFrame.iloc[0]['crddb_linevoltage'] * 1e3 / np.sqrt(3)) / dataFrame.iloc[0]["crddb_steadystatecurrent"]
        x_abc_term2 = 0

        line2neutral_kv = 0
        line2neutral_deg = 0

        current_mag_ka = dataFrame.iloc[0]["crddb_contributionfaultcurrent_term2_mod"]
        current_ang_deg = dataFrame.iloc[0]["crddb_contributionfaultcurrent_term2_phase"]

        # Create phase dictionaries using the create_phase_dict function
        c1_phase_a_term2 = create_phase_dict('a', 1, 1, ground_point_LT, cartesian1, r_abc_term2, x_abc_term2, polar2, 
                                        line2neutral_kv, line2neutral_deg, current_mag_ka, current_ang_deg)

        c1_phase_b_term2 = create_phase_dict('b', 2, 2, ground_point_LT, cartesian1, r_abc_term2, x_abc_term2, polar2,
                                        line2neutral_kv, line2neutral_deg, current_mag_ka, current_ang_deg)

        c1_phase_c_term2 = create_phase_dict('c', 3, 3, ground_point_LT, cartesian1, r_abc_term2, x_abc_term2, polar2, 
                                        line2neutral_kv, line2neutral_deg, current_mag_ka, current_ang_deg)

        phase_pipe_term2 = create_phase_dict('pipe', 8, 8, ground_point_DT, cartesian1, 0, 0, polar2, 0, 0, 0, 0)

        
        # Get values
        r_abc_term1 = 0  
        x_abc_term1 = 0  
        line2neutral_kv = dataFrame.iloc[0]['crddb_linevoltage'] / np.sqrt(3)  # pu
        line2neutral_deg = phases_c2

        # Create phase dictionaries
        c2__phase_a_term1 = create_phase_dict('a', 4, 4, ground_point_LT, cartesian1, r_abc_term1, x_abc_term1, polar2,
                                        line2neutral_kv, line2neutral_deg[0], 0, 0)
        c2__phase_b_term1 = create_phase_dict('b', 5, 5, ground_point_LT, cartesian1, r_abc_term1, x_abc_term1, polar2,
                                        line2neutral_kv, line2neutral_deg[1], 0, 0)
        c2__phase_c_term1 = create_phase_dict('c', 6, 6, ground_point_LT, cartesian1, r_abc_term1, x_abc_term1, polar2,
                                        line2neutral_kv, line2neutral_deg[2], 0, 0)
        

            # Get values (assuming r_pipe and x_pipe are already defined)
        r_abc_term2 = (dataFrame.iloc[0]['crddb_linevoltage'] * 1e3 / np.sqrt(3)) / dataFrame.iloc[0]["crddb_steadystatecurrent"]
        x_abc_term2 = 0

        line2neutral_kv = 0
        line2neutral_deg = 0

        current_mag_ka = dataFrame.iloc[0]["crddb_contributionfaultcurrent_term2_mod"]
        current_ang_deg = dataFrame.iloc[0]["crddb_contributionfaultcurrent_term2_phase"]

        # Create phase dictionaries using the create_phase_dict function
        c2__phase_a_term2 = create_phase_dict('a', 4, 4, ground_point_LT, cartesian1, r_abc_term2, x_abc_term2, polar2, 
                                        line2neutral_kv, line2neutral_deg, current_mag_ka, current_ang_deg)

        c2__phase_b_term2 = create_phase_dict('b', 5, 5, ground_point_LT, cartesian1, r_abc_term2, x_abc_term2, polar2,
                                        line2neutral_kv, line2neutral_deg, current_mag_ka, current_ang_deg)

        c2__phase_c_term2 = create_phase_dict('c', 6, 6, ground_point_LT, cartesian1, r_abc_term2, x_abc_term2, polar2, 
                                        line2neutral_kv, line2neutral_deg, current_mag_ka, current_ang_deg)


        
        energization_info_lt = [c1_phase_a_term1, c1_phase_b_term1, c1_phase_c_term1, c2__phase_a_term1, c2__phase_b_term1, c2__phase_c_term1, sw_, phase_pipe_term1]
        energization_info_dt = [c1_phase_a_term2, c1_phase_b_term2, c1_phase_c_term2, c2__phase_a_term2, c2__phase_b_term2, c2__phase_c_term2, sw_, phase_pipe_term2]
        return energization_info_lt, energization_info_dt