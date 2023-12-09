from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeSerice
import requests
from selenium.webdriver.common.by import By

from selenium import webdriver
import requests
import pyautogui as py
import time

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