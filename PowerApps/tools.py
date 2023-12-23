from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
import requests
import pyautogui as py
import time
import numpy as np
import pandas as pd
import clipboard
from typing import Union, Dict, Any, Tuple, List




def take_request(user: str, password: str) -> tuple[str, str]:
    """
    Initiates the process to obtain an access token for accessing Dynamics CRM services.

    Args:
    - user (str): User login or username for authentication.
    - password (str): User password for authentication.

    Returns:
    - str, str: A tuple containing the obtained access token and the callback URL used in the process.
    """
    # Initialize a Chrome WebDriver
    driver = webdriver.Chrome()

    # Your Azure AD and OAuth2.0 parameters
    url = 'https://org425ee2cf.api.crm.dynamics.com'
    client_id = '51f81489-12ee-4a9e-aaae-a2591f45987d'
    callback_base_url = 'https://localhost'

    # Construct the authorization URL with query parameters
    auth_url = f'https://login.microsoftonline.com/common/oauth2/authorize?' \
            f'client_id={client_id}&response_type=code&redirect_uri={callback_base_url}&resource={url}'

    # Obtain the callback URL using provided credentials
    callback_url = take_callback_url(auth_url, driver, user, password)

    # Get access token using the obtained callback URL
    access_token = get_access_token(callback_url, client_id, callback_base_url, url)
    
    return access_token, callback_url




def take_callback_url(auth_url: str, driver: WebDriver, user: str, password: str) -> str:
    """
    Navigates to the authentication URL, enters user credentials, and retrieves the callback URL.

    Args:
    - auth_url (str): The URL for authorization/authentication.
    - driver: WebDriver instance for browser automation.
    - user (str): User login or username for authentication.
    - password (str): User password for authentication.

    Returns:
    - str: The callback URL obtained after successful authentication.
    """
    driver.get(auth_url)

    time.sleep(3)
    py.write(user)
    time.sleep(1)
    py.press('enter')

    time.sleep(3)
    py.write(password)
    time.sleep(1)
    py.press('enter')

    time.sleep(3)
    py.hotkey('ctrl', 'l')
    py.hotkey('ctrl', 'c')
    callback_url = str(clipboard.paste())
    print(callback_url)
    
    return callback_url




def get_access_token(callback_url: str, client_id: str, callback_base_url: str, url: str) -> str:
    """
    Obtains an access token from a callback URL using OAuth2.0 authentication.

    Args:
    - callback_url (str): Callback URL received after the initial authentication step.
    - client_id (str): Client ID required for OAuth2.0 authentication.
    - callback_base_url (str): Base URL to which the callback occurs.
    - url (str): The resource URL to request the access token.

    Returns:
    - str: The obtained access token used for subsequent requests to the specified URL.
    """
    start_index = callback_url.find('code=')
    end_index = callback_url.find('&', start_index)
    authorization_code = callback_url[start_index + len('code='):end_index]

    token_url = 'https://login.microsoftonline.com/common/oauth2/token'

    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'code': authorization_code,
        'redirect_uri': callback_base_url,
        'resource': url
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(token_url, data=data, headers=headers)

    access_token = response.json().get('access_token')
    print(access_token)
    return access_token




def request_autorow(access_token: str) -> dict:
    """
    Retrieves autorow report input sessions from Dynamics CRM using the provided access token.

    Args:
    - access_token (str): Access token used for authentication and authorization.

    Returns:
    - dict: JSON response containing autorow report input sessions retrieved from Dynamics CRM.
    """
    url = 'https://org425ee2cf.crm.dynamics.com/api/data/v9.2/crddb_autorowreportinputsessions?$top=10'
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    print(response)
    return response.json()




def check_equal_columns(df: pd.DataFrame) -> bool:
    """
    Checks for duplicate column names within the DataFrame.

    Args:
    - df (pandas.DataFrame): Input DataFrame to check for duplicate columns.

    Returns:
    - bool: True if duplicate columns exist, False otherwise.
    """
    # Check for duplicate columns
    duplicates = df.columns[df.columns.duplicated()]
    
    if duplicates.any():
        print(f'The dataset has columns with the same names: {duplicates.tolist()}')
        return True
    else:
        print('The dataset does not have columns with the same names.')
        return False




def downloaded_file(id: str or int, column: str, name: str, access_token: str) -> None:
    """
    Downloads a file associated with a specific ID and column from Dynamics CRM.

    Args:
    - id (str or int): Identifier associated with the file to download.
    - column (str): The column name related to the file to download.
    - name (str): Name of the file to be saved after downloading.
    - access_token (str): Access token for authentication and authorization.

    Returns:
    - None
    """
    api_endpoint = f'https://org425ee2cf.crm.dynamics.com/api/data/v9.0/crddb_autorowreportinputsessions({id})/crddb_coordinatesfile_{column}/$value'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(api_endpoint, headers=headers)
    if response.status_code == 200:
        file_content = response.content
        # Write the binary data to a file
        with open(name, 'wb') as file:
            file.write(file_content)
        print("File downloaded successfully.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")




def request_conductors(access_token: str) -> Union[dict, None]:
    """
    Retrieves conductor information from Dynamics CRM using the provided access token.

    Args:
    - access_token (str): Access token used for authentication and authorization.

    Returns:
    - dict or None: JSON response containing conductor information retrieved from Dynamics CRM.
      Returns None if the request fails.
    """
    api_cond = 'https://org425ee2cf.crm.dynamics.com/api/data/v9.2/crddb_conductors?$top=10'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
       
    response = requests.get(api_cond, headers=headers)
    if response.status_code == 200:
        data_cond = response.json()  # Assuming the response is in JSON format
        print(data_cond)
    
        print("Request Done.")
        return data_cond
    else:
        print(f"Request Failed. \nStatus code: {response.status_code}")
        return None



        
def request_soil(access_token: str) -> Union[dict, None]:
    """
    Retrieves soil fit input sessions from Dynamics CRM using the provided access token.

    Args:
    - access_token (str): Access token used for authentication and authorization.

    Returns:
    - dict or None: JSON response containing soil fit input sessions retrieved from Dynamics CRM.
      Returns None if the request fails.
    """
    api_cond = 'https://org425ee2cf.crm.dynamics.com/api/data/v9.2/crddb_soilfitinputsessions?$top=10'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
       
    response = requests.get(api_cond, headers=headers)
    if response.status_code == 200:
        data_soil = response.json()  # Assuming the response is in JSON format
        print(data_soil)
    
        print("Request Done.")
        return data_soil
    else:
        print(f"Request Failed. \nStatus code: {response.status_code}")
        return None



    
def request_obs(access_token: str) -> Union[dict, None]:
    """
    Retrieves observation points from Dynamics CRM using the provided access token.

    Args:
    - access_token (str): Access token used for authentication and authorization.

    Returns:
    - dict or None: JSON response containing observation points retrieved from Dynamics CRM.
      Returns None if the request fails.
    """
    api_cond = 'https://org425ee2cf.crm.dynamics.com/api/data/v9.2/new_obspoints?$top=10'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(api_cond, headers=headers)
    if response.status_code == 200:
        data_obs = response.json()  # Assuming the response is in JSON format
        print(data_obs)
        print("Request Done.")
        return data_obs
    else:
        print(f"Failed to request. Status code: {response.status_code}")
        return None

        

        
def request_coating(access_token: str) -> Union[dict, None]:
    """
    Requests coating data from Dynamics CRM using the provided access token.

    Args:
    - access_token (str): Access token used for authentication and authorization.

    Returns:
    - dict or None: JSON response containing coating data retrieved from Dynamics CRM.
      Returns None if the request fails.
    """
    api_cond = 'https://org425ee2cf.crm.dynamics.com/api/data/v9.2/crddb_coatings?$top=10'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
       
    response = requests.get(api_cond, headers=headers)
    if response.status_code == 200:
        data_cond = response.json()  # Assuming the response is in JSON format
        print(data_cond)
        print("Request Done.")
        return data_cond
    else:
        print(f"Request Failed. \nStatus code: {response.status_code}")
        return None




def df_columns(data: dict, column: str) -> Union[pd.DataFrame, None]:
    """
    Extracts a specific column from a DataFrame contained within the provided data dictionary.

    Args:
    - data (dict): Dictionary containing a DataFrame under the 'value' key.
    - column (str): Column name to extract from the DataFrame.

    Returns:
    - pandas DataFrame or None: Returns the specified column as a pandas Series.
      Returns None if the DataFrame or specified column is not found.
    """
    dataFrame = pd.DataFrame(data['value'])
    dataFrame = dataFrame[column]
    return dataFrame



        
def save_to_txt_file(file_name: str, content: str) -> None:
    """
    Saves content to a text file with the provided filename.

    Args:
    - file_name (str): Name of the file to be created or overwritten.
    - content (str): Content to be written to the file.

    Returns:
    - None
    """
    with open(file_name, 'w') as file:
        file.write(content)
    print(f"Content successfully saved to '{file_name}'.")



    
def create_string_duct(duct: dict, coating: dict) -> str:
    """
    Creates a string representing duct characteristics.

    Args:
    - duct (dict): Dictionary containing duct information.
    - coating (dict): Dictionary containing coating information.

    Returns:
    - str: String representing the duct characteristics.
    """
    type_ = "AREARESISTANCE" if coating["crddb_area_resistance"] is None else "RESISTIVITY"
    
    duct_dict = {
        'cross_section': duct['crddb_cross_section'],
        'Conductor_Name': duct["crddb_name"],
        'inner_Radius': duct["crddb_innerradius"],
        'outer_Radius': duct["crddb_outerradius"],
        'relative_resistivity': duct["crddb_resistivity"],
        'dc_Resistance': duct["crddb_dc_resistance"],
        'ac_Resistance': duct["crddb_ac_resistence"],
        'relative_permeability': duct["crddb_relativepermeability"],
        'GMR': '',
        'X': 0.577875018119812
    }
    
    duct_string = f""" COMPONENT-TYPE,1,{duct_dict['Conductor_Name']}
         GROUP-COMPONENT,CONDUCTOR,1,{duct_dict['Conductor_Name']},0,0,0,0
         LAYER,CONDUCTOR,1,{duct_dict['Conductor_Name']}_Conductor
             CONDUCTOR-CHARACTERISTICS,{duct_dict['inner_Radius']},{duct_dict['outer_Radius']},2,
             {duct_dict['relative_resistivity']},{duct_dict['dc_Resistance']},{duct_dict['ac_Resistance']} ,
             2,{duct_dict['relative_permeability']},{duct_dict['GMR']},{duct_dict['X']},1,7,0.00152399996295571,
             0,,,51.076099395752,{duct_dict['cross_section']} ,,60,0,0
             DB-CONDUCTOR_INFO,SYNCHRONIZEDWITHDB,3/8 EHS-CG,Steel,60.0
         LAYER,INSULATION,2,Pipes-Steel_10" 140_Conductor - Insulation
             INSULATION-CHARACTERISTICS,{type_},{duct_dict['outer_Radius']},
             {duct_dict['outer_Radius'] + coating['crddb_thickness']},
             {coating['crddb_area_resistance']},{coating['crddb_permittivity']},{coating['crddb_permeability']} ,
             {coating['crddb_permeability']}"""
    return duct_string




def create_string_conductor(conductor: dict, idx: int) -> str:
    """
    Creates a string representing conductor characteristics.

    Args:
    - conductor (dict): Dictionary containing conductor information.

    Returns:
    - str: String representing the conductor characteristics.
    """
    conductor_dict = {
        'Conductor_Name': conductor["crddb_name"],
        'cross_section': conductor["crddb_cross_section"],
        'inner_Radius': conductor["crddb_innerradius"],
        'outer_Radius': conductor["crddb_outerradius"],
        'relative_resistivity': conductor["crddb_resistivity"],
        'dc_Resistance': conductor["crddb_dc_resistance"],
        'ac_Resistance': conductor["crddb_ac_resistence"],
        'relative_permeability': conductor["crddb_relativepermeability"],
        'GMR': conductor["crddb_gmr"],
        'X': 0.256067007780075
    }
    
    conductor_string = f"""  COMPONENT-TYPE,{idx},{conductor_dict['Conductor_Name']}
        GROUP-COMPONENT,CONDUCTOR,1,{conductor_dict['Conductor_Name']},0,0,0,0
        LAYER,CONDUCTOR,1,{conductor_dict['Conductor_Name']}_Conductor
            CONDUCTOR-CHARACTERISTICS,{conductor_dict["inner_Radius"]},{conductor_dict["outer_Radius"]},1,
            {conductor_dict["relative_resistivity"]},{conductor_dict["dc_Resistance"]},
            {conductor_dict["ac_Resistance"]},1,{conductor_dict["relative_permeability"]},{conductor_dict["GMR"]},
            {conductor_dict["X"]},1,26,0.00198628008365631,0.00463549979031086,7,0.00154432002454996,
            322.265960693359,{conductor_dict['cross_section']},,60,0,0
            DB-CONDUCTOR_INFO,SYNCHRONIZEDWITHDB,{conductor_dict['Conductor_Name']},ACSR,60,0"""
    return conductor_string




def remove_nan_from_dict(dictionary: dict) -> dict:    
    """
    Recursively removes NaN values from a nested dictionary by replacing them with an empty string.

    Args:
    - dictionary (dict): The nested dictionary containing NaN values.

    Returns:
    - dict: The modified dictionary with NaN values replaced by empty strings.
    """

    keys_to_remove = []  # List to store keys with NaN values

    for key, value in dictionary.items():
        if isinstance(value, dict):
            remove_nan_from_dict(value)  # Checks for values in nested dictionaries
        elif pd.isnull(value):  # Checks if the value is NaN
            keys_to_remove.append(key)  # Adds the key to the removal list for NaN values

    # Removes keys with NaN values and replaces the NaN value with an empty string
    for key in keys_to_remove:
        dictionary[key] = ''  # Replaces NaN value with an empty string

        


def calculate_vector(point1: np.ndarray or list or tuple, point2: np.ndarray or list or tuple) -> np.ndarray:
    """
    Calculate the vector between two points.

    Args:
    - point1 (numpy.ndarray or array-like): The coordinates of the first point.
    - point2 (numpy.ndarray or array-like): The coordinates of the second point.

    Returns:
    - numpy.ndarray: The vector resulting from subtracting point1 from point2.
    """
    return point2 - point1




def create_orientation_points(df: pd.DataFrame, n_before: int, n_after: int, distance: float) -> pd.DataFrame:
    """
    Create orientation points before and after the coordinates in the DataFrame.

    Args:
    - df (pandas.DataFrame): DataFrame containing coordinates.
    - n_before (int): Number of points to create before the first coordinate.
    - n_after (int): Number of points to create after the last coordinate.
    - distance (float): Distance between the points.

    Returns:
    - pandas.DataFrame: DataFrame with additional points created before and after the original coordinates.
    """
    if len(df) < 2:
        return pd.DataFrame()

    coordinates = df.to_numpy()

    # Calculate vectors
    vector_start = calculate_vector(coordinates[0], coordinates[1])
    vector_end = calculate_vector(coordinates[-2], coordinates[-1])

    # Calculate normalized vectors
    norm_vector_start = vector_start / np.linalg.norm(vector_start)
    norm_vector_end = vector_end / np.linalg.norm(vector_end)

    # Create points before the first coordinate
    points_before = []
    for i in range(int(n_before), 0, -1):
        new_point = coordinates[0] - i * distance * norm_vector_start
        points_before.append(np.append(new_point, 'Before'))

    # Create points after the last coordinate
    points_after = []
    for i in range(1, int(n_after) + 1):
        new_point = coordinates[-1] + i * distance * norm_vector_end
        points_after.append(np.append(new_point, 'After'))

    # Convert lists to DataFrames
    df_before = pd.DataFrame(np.array(points_before), columns=list(df.columns) + ['Label'])
    df_after = pd.DataFrame(np.array(points_after), columns=list(df.columns) + ['Label'])

    # Include a Label column for the original points
    df['Label'] = 'Original'

    # Combine DataFrames
    combined_df = pd.concat([df_before, df, df_after], ignore_index=True)

    return combined_df




def create_phase_dict(name: str, id: int, ph: str, ground_point: Tuple[float, float], cartesian1: Tuple[float, float],
                      R: float, X: float, polar2: float, line2neutral_kv: float, line2neutral_deg: float,
                      current_mag_ka: float, current_ang_deg: float) -> Dict[str, Any]:
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




def add_new_row(dataFrame: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a new row to the beginning of the DataFrame by incrementing the first row by 0.01.

    Args:
    - dataFrame (pd.DataFrame): The DataFrame to which a new row will be added.

    Returns:
    - pd.DataFrame: DataFrame with a new row added at the beginning.
    """
    new_row = dataFrame.iloc[0].copy() + 0.01
    dataFrame = pd.concat([pd.DataFrame(new_row).transpose(), dataFrame], ignore_index=True)
    return dataFrame




def generate_points(dataFrame: pd.DataFrame, name: str = '', rho: float = 1, xs: float = 1,
                    type_: int = -2, is_DT: bool = False) -> str:
    """
    Generates either LT (Line-to-Transverse) or DT (Distribution Transformer) points
    based on the DataFrame coordinates.

    Args:
    - dataFrame (pd.DataFrame): DataFrame containing coordinates.
    - name (str): Name associated with the points.
    - rho (int/float): Value for 'rho' in the generated points.
    - xs (int/float): Value for 'xs' in the generated points.
    - type_ (int): Type of point (default value is -2).
    - is_DT (bool): If True, generates DT points; otherwise, generates LT points.

    Returns:
    - str: String containing points information formatted for use.
    """
    points = []
    for index, row in dataFrame.iterrows():
        x = row[0]
        y = row[1]

        if is_DT:
            something = 10 if index == 0 else 0
            point_info = f'      POINT,{index+1},{name},{x},{y},0,{something},{rho},{type_},{xs},0'
        else:
            x = x + 0.01 if index == 0 else x
            type_ = -1 if index == 0 else -2
            point_info = f'      POINT,{index+1},{name},{x},{y},0,0,{rho},{type_},{xs},0'

        points.append(point_info)

    return '\n'.join(points)




def generate_leakage_info(energization_info: List[Dict[str, str]], data_df: pd.DataFrame) -> str:
    """
    Generate leakage information based on energization details and tower ground impedance data.

    Args:
    - energization_info (list): List containing energization information, each item being a dictionary with keys like 'name' and 'id'.
    - data_df (pd.DataFrame): DataFrame containing tower ground impedance data.

    Returns:
    - str: String containing formatted leakage information based on the given data.
    """
    lista = []
    r_sw = data_df.iloc[0]['crddb_groundimpedance_towers_r']   
    x_sw = data_df.iloc[0]['crddb_groundimpedance_towers_x']
    
    for i in energization_info:
        if i["name"] == 'sw':
            tower_ground_imped = [r_sw, x_sw]
            leakage_type = "OHMSPERTOWER"
        else:
            tower_ground_imped = [9999999, 9999999]
            leakage_type = "COMPUTED"

        leakage_info = f'    LEAKAGE,{leakage_type},{i["id"]},{i["name"]},0,{tower_ground_imped[0]},{tower_ground_imped[1]}'
        lista.append(leakage_info)

    return '\n'.join(lista)




def add_condtype_id(driver_info_list: List[Dict[str, Any]]) -> None:
    """
    Adds 'condtype_id' to each dictionary in the list based on 'condtype_value' uniqueness.

    Args:
    - driver_info_list (List[Dict[str, Any]]): List of dictionaries containing 'condtype_value' keys.

    Returns:
    - None
    """
    # Extract unique condtype_values from driver_info_list
    condtype_values = [d['condtype_value'] for d in driver_info_list]
    unique_condtype_values = list(set(condtype_values))

    # Create a dictionary mapping condtype_values to unique integer IDs
    condtype_id_mapping = {value: index + 1 for index, value in enumerate(unique_condtype_values)}

    # Update each dictionary in driver_info_list with condtype_id based on the mapping
    for driver_info in driver_info_list:
        condtype_value = driver_info.get("condtype_value")
        if condtype_value in condtype_id_mapping:
            driver_info["condtype_id"] = condtype_id_mapping[condtype_value]
        else:
            pass  # Do something if the condtype_value is not found in mapping




def generate_total_cross_section(circuit_type: int,
                                 energization_info_lt: List[Dict[str, Any]],
                                 phase_cross_section: str,
                                 condutores_rowCAD: str,
                                 condutores: List[Dict[str, Any]]) -> str:
    """
    Generates the total cross-section based on the provided parameters.

    Args:
    - circuit_type (int): Type of circuit.
    - energization_info_lt (List[Dict[str, Any]]): Information about energization for LT.
    - phase_cross_section (str): Phase cross-section details.
    - condutores_rowCAD (str): Condutores rowCAD details.
    - condutores (List[Dict[str, Any]]): List of dictionaries containing conductor details.

    Returns:
    - str: String representing the total cross-section generated based on the given parameters.
    """
    if circuit_type==1:
        total_cross_section1_LT = f"""CROSSSECTION
OPTIONS
    CONFIGURATION-MODE,ROW
    UNITS,METRIC
{phase_cross_section}
{condutores_rowCAD}
SYSTEM
    SUBSET,1,Set #1
    COMPONENT,1,Component #1,{condutores[0]['crddb_c1a_horizontal']},{condutores[0]['crddb_c1a_vertical']},1
        INFO-GROUPCOMPONENT,{condutores[0]['condtype_id']},{condutores[0]['crddb_name']}
        INFO-PHASE-CIRCUIT,1,{energization_info_lt[0]["id"]},0,0
    COMPONENT,2,Component #2,{condutores[1]['crddb_c1b_horizontal']},{condutores[1]['crddb_c1b_vertical']},1
        INFO-GROUPCOMPONENT,{condutores[1]['condtype_id']},{condutores[1]['crddb_name']}
        INFO-PHASE-CIRCUIT,1,{energization_info_lt[1]["id"]},0,0
    COMPONENT,3,Component #3,{condutores[2]['crddb_c1c_horizontal']},{condutores[2]['crddb_c1c_vertical']},1
        INFO-GROUPCOMPONENT,{condutores[2]['condtype_id']},{condutores[2]['crddb_name']}
        INFO-PHASE-CIRCUIT,1,{energization_info_lt[2]["id"]},0,0
    COMPONENT,4,Component #4,{condutores[3]['crddb_shieldwirehorizontal1']},{condutores[3]['crddb_shieldwirevertical1']},1
        INFO-GROUPCOMPONENT,{condutores[3]['condtype_id']},{condutores[3]['crddb_name']}
        INFO-PHASE-CIRCUIT,1,{energization_info_lt[-2]["id"]},0,0
    COMPONENT,5,Component #5,{condutores[4]['crddb_shieldwirehorizontal2']},{condutores[4]['crddb_shieldwirevertical2']},1
        INFO-GROUPCOMPONENT,{condutores[4]['condtype_id']},{condutores[4]['crddb_name']}
        INFO-PHASE-CIRCUIT,1,{energization_info_lt[-2]["id"]},0,0
ENDPROGRAM"""
            
    elif circuit_type==2:
        total_cross_section1_LT = f"""CROSSSECTION
OPTIONS
    CONFIGURATION-MODE,ROW
    UNITS,METRIC
{phase_cross_section}
{condutores_rowCAD}
SYSTEM
    SUBSET,1,Set #1
    COMPONENT,1,Component #1,{condutores[0]['crddb_c1a_horizontal']},{condutores[0]['crddb_c1a_vertical']},1
        INFO-GROUPCOMPONENT,{condutores[0]['condtype_id']},{condutores[0]['crddb_name']}
        INFO-PHASE-CIRCUIT,1,{energization_info_lt[0]["id"]},0,0
    COMPONENT,2,Component #2,{condutores[1]['crddb_c1b_horizontal']},{condutores[1]['crddb_c1b_vertical']},1
        INFO-GROUPCOMPONENT,{condutores[1]['condtype_id']},{condutores[1]['crddb_name']}
        INFO-PHASE-CIRCUIT,1,{energization_info_lt[1]["id"]},0,0
    COMPONENT,3,Component #3,{condutores[2]['crddb_c1c_horizontal']},{condutores[2]['crddb_c1c_vertical']},1
        INFO-GROUPCOMPONENT,{condutores[2]['condtype_id']},{condutores[2]['crddb_name']}
        INFO-PHASE-CIRCUIT,1,{energization_info_lt[2]["id"]},0,0
    COMPONENT,4,Component #4,{condutores[3]['crddb_c2a_horizontal']},{condutores[3]['crddb_c2a_vertical']},1
        INFO-GROUPCOMPONENT,{condutores[3]['condtype_id']},{condutores[3]['crddb_name']}
        INFO-PHASE-CIRCUIT,1,{energization_info_lt[3]["id"]},0,0
    COMPONENT,5,Component #5,{condutores[4]['crddb_c2b_horizontal']},{condutores[4]['crddb_c2b_vertical']},1
        INFO-GROUPCOMPONENT,{condutores[4]['condtype_id']},{condutores[4]['crddb_name']}
        INFO-PHASE-CIRCUIT,1,{energization_info_lt[4]["id"]},0,0
    COMPONENT,6,Component #6,{condutores[5]['crddb_c2c_horizontal']},{condutores[5]['crddb_c2c_vertical']},1
        INFO-GROUPCOMPONENT,{condutores[5]['condtype_id']},{condutores[5]['crddb_name']}
        INFO-PHASE-CIRCUIT,1,{energization_info_lt[5]["id"]},0,0
    COMPONENT,7,Component #4,{condutores[6]['crddb_shieldwirehorizontal1']},{condutores[6]['crddb_shieldwirevertical1']},1
        INFO-GROUPCOMPONENT,{condutores[6]['condtype_id']},{condutores[6]['crddb_name']}
        INFO-PHASE-CIRCUIT,1,{energization_info_lt[-2]["id"]},0,0
    COMPONENT,8,Component #5,{condutores[7]['crddb_shieldwirehorizontal2']},{condutores[7]['crddb_shieldwirevertical2']},1
        INFO-GROUPCOMPONENT,{condutores[7]['condtype_id']},{condutores[7]['crddb_name']}
        INFO-PHASE-CIRCUIT,1,{energization_info_lt[-2]["id"]},0,0
ENDPROGRAM"""
    return total_cross_section1_LT