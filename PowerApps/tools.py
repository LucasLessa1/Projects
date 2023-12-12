from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeSerice
import requests
from selenium.webdriver.common.by import By

from selenium import webdriver
import requests
import pyautogui as py
import time
        
import numpy as np
import pandas as pd

import clipboard
import pandas as pd



def take_callback_url(auth_url, driver, user, password):
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



def get_access_token(callback_url, client_id, callback_base_url, url):
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

def make_authenticated_request(access_token, url):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    print(response)
    return response.json()



def check_equal_columns(df):
    
    # Verificar se há colunas duplicadas
    duplicatas = df.columns[df.columns.duplicated()]
    
    if duplicatas.any():
        print(f'O dataset possui colunas com nomes iguais: {duplicatas.tolist()}')
        return True
    else:
        print('O dataset não possui colunas com nomes iguais.')
        return False


def downloaded_file(id, column, name, access_token):

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


def request_conductors(access_token):
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
        
def request_soil(access_token):
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
    
    
def request_obs(access_token):
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
        
        
def request_coating(access_token):
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
    
        
def save_to_txt_file(file_name, content):
    with open(file_name, 'w') as file:
        file.write(content)
    print(f"Content successfully saved to '{file_name}'.")
    
def criar_string_duto(duto, coating):
    
    type_ = "AREARESISTANCE"
    
    if coating["crddb_area_resistance"] == None:
        type_ = "RESISTIVITY"
    
    duto_dict = {'cross_section': duto['crddb_cross_section'],'Conductor_Name' : duto["crddb_name"], 'inner_Radius' : duto["crddb_innerradius"], 'outer_Radius' : duto["crddb_outerradius"], 'relative_resistivity' : duto["crddb_resistivity"], 'dc_Resistance' : duto["crddb_dc_resistance"], 'ac_Resistance' : duto["crddb_ac_resistence"], 'relative_permeability' : duto["crddb_relativepermeability"], 'GMR' : '', 'X' : 0.577875018119812}
    duto_string = f"""  COMPONENT-TYPE,1,{duto_dict['Conductor_Name']}
        GROUP-COMPONENT,CONDUCTOR,1,{duto_dict['Conductor_Name']},0,0,0,0
        LAYER,CONDUCTOR,1,{duto_dict['Conductor_Name']}_Conductor
            CONDUCTOR-CHARACTERISTICS,{duto_dict['inner_Radius']},{duto_dict['outer_Radius']},2,{duto_dict['relative_resistivity']},{duto_dict['dc_Resistance']},{duto_dict['ac_Resistance']},2,{duto_dict['relative_permeability']},{duto_dict['GMR']},{duto_dict['X']},1,7,0.00152399996295571,0,,,51.076099395752,{duto_dict['cross_section']},,60,0,0
            DB-CONDUCTOR_INFO,SYNCHRONIZEDWITHDB,3/8 EHS-CG,Steel,60,0
        LAYER,INSULATION,2,Pipes-Steel_10" 140_Conductor - Insulation
            INSULATION-CHARACTERISTICS,{type_},{duto_dict['outer_Radius']},{duto_dict['outer_Radius'] + coating['crddb_thickness']},{coating['crddb_area_resistance']},{coating['crddb_permittivity']},{coating['crddb_permittivity']}"""
    return duto_string

def criar_string_condutor(conductor):
    conductor_dict = {'Conductor_Name' : conductor["crddb_name"], 'cross_section': conductor["crddb_cross_section"], 'inner_Radius' : conductor["crddb_innerradius"], 'outer_Radius' : conductor["crddb_outerradius"], 'relative_resistivity' : conductor["crddb_resistivity"], 'dc_Resistance' : conductor["crddb_dc_resistance"], 'ac_Resistance' : conductor["crddb_ac_resistence"], 'relative_permeability' : conductor["crddb_relativepermeability"], 'GMR' : conductor["crddb_gmr"], 'X' : 0.256067007780075}
    conductor_string = f"""  COMPONENT-TYPE,1,{conductor_dict['Conductor_Name']}
        GROUP-COMPONENT,CONDUCTOR,1,{conductor_dict['Conductor_Name']},0,0,0,0
        LAYER,CONDUCTOR,1,{conductor_dict['Conductor_Name']}_Conductor
            CONDUCTOR-CHARACTERISTICS,{conductor_dict["inner_Radius"]},{conductor_dict["outer_Radius"]},1,{conductor_dict["relative_resistivity"]},{conductor_dict["dc_Resistance"]},{conductor_dict["ac_Resistance"]},1,{conductor_dict["relative_permeability"]},{conductor_dict["GMR"]},{conductor_dict["X"]},1,26,0.00198628008365631,0.00463549979031086,7,0.00154432002454996,322.265960693359,{conductor_dict['cross_section']},,60,0,0
            DB-CONDUCTOR_INFO,SYNCHRONIZEDWITHDB,{conductor_dict['Conductor_Name']},ACSR,60,0"""
    return conductor_string


def remove_nan_from_dict(dictionary):
    keys_to_remove = []  # Lista para armazenar as chaves a serem removidas

    for key, value in dictionary.items():
        if isinstance(value, dict):
            remove_nan_from_dict(value)  # Verifica os valores nos dicionários aninhados
        elif pd.isnull(value):  # Verifica se o valor é NaN
            keys_to_remove.append(key)  # Adiciona a chave à lista de remoção

    # Remove as chaves que possuem valores NaN
    for key in keys_to_remove:
        dictionary[key] = ''  # Substitui o valor NaN por string vazia
        

def calculate_vector(point1, point2):
    return point2 - point1

def create_orientation_points(df, n_before, n_after, distance):
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

