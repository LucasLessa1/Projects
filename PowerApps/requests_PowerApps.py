from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeSerice
import requests
from selenium.webdriver.common.by import By

from selenium import webdriver
import requests

# Initialize a Chrome WebDriver
driver = webdriver.Chrome()

# Your Azure AD and OAuth2.0 parameters
url = 'https://org425ee2cf.api.crm.dynamics.com'
client_id = '51f81489-12ee-4a9e-aaae-a2591f45987d'
callback_base_url = 'https://localhost'


# Construct the authorization URL with query parameters
auth_url = f'https://login.microsoftonline.com/common/oauth2/authorize?' \
           f'client_id={client_id}&response_type=code&redirect_uri={callback_base_url}&resource={url}'


# Open the authorization URL in a browser
driver.get(auth_url)

# Wait for the user to complete the authorization and extract the callback URL with the authorization code
callback_url = input('Enter the callback URL after completing the authorization: ')

start_index = callback_url.find('code=')
end_index = callback_url.find('&', start_index)
authorization_code = callback_url[start_index + len('code='):end_index]

# Parse the authorization code from the callback URL
# authorization_code = callback_url.split('code=')[1]

# Exchange the authorization code for an access token
token_url = 'https://login.microsoftonline.com/common/oauth2/token'


data = {
    'grant_type': 'authorization_code',
    'client_id': client_id,
    'code': authorization_code,
    'redirect_uri': callback_base_url,
    'resource': url  # Add the 'resource' parameter
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.post(token_url, data=data, headers=headers)

access_token = response.json().get('access_token')
# Display the access token
print('Access token:')
print(access_token)


url = 'https://org425ee2cf.crm.dynamics.com/api/data/v9.2/crddb_autorowreportinputsessions?$top=10'

# Create the headers with the Authorization token
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Send the HTTP GET request
response = requests.get(url, headers=headers)


# Process the response as needed
data = response.json()  # Assuming the response is in JSON format
print(data)

