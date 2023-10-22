import webbrowser
import requests

# Define the necessary parameters
url = 'https://org425ee2cf.api.crm.dynamics.com'
client_id = '51f81489-12ee-4a9e-aaae-a2591f45987d'
# client_id = '673d9e85-b0d1-4f5a-ae7a-3dccf0c31a9f'
callback_base_url = 'https://localhost'

# Construct the authorization URL with query parameters
auth_url = f'https://login.microsoftonline.com/common/oauth2/authorize?' \
           f'client_id={client_id}&response_type=code&redirect_uri={callback_base_url}&resource={url}'

# Open the authorization URL in a browser
webbrowser.open(auth_url)

# Wait for the user to complete the authorization and extract the callback URL with the authorization code
callback_url = input('Enter the callback URL after completing the authorization: ')

# Parse the authorization code from the callback URL
authorization_code = callback_url.split('code=')[1]

# Exchange the authorization code for an access token
token_url = 'https://login.microsoftonline.com/common/oauth2/token'

data = {
    'grant_type': 'authorization_code',
    'client_id': client_id,
    'code': authorization_code,
    'redirect_uri': callback_base_url
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.post(token_url, data=data, headers=headers)

if response.status_code == 200:
    access_token = response.json()['access_token']

    # Use the access token for subsequent API requests
    # (perform your desired actions with the obtained access token)

    # Display the access token
    print('Access token:')
    print(access_token)
else:
    print(f'Error: {response.status_code} - {response.text}')

# You can also refresh the token if needed
# refresh_data = {
#     'grant_type': 'refresh_token',
#     'client_id': client_id,
#     'refresh_token': response.json()['refresh_token'],
#     'redirect_uri': callback_base_url
# }
# refresh_response = requests.post(token_url, data=refresh_data, headers=headers)
# if refresh_response.status_code == 200:
#     new_access_token = refresh_response.json()['access_token']
#     print('Refreshed Access token:')
#     print(new_access_token)
# else:
#     print(f'Error refreshing token: {refresh_response.status_code} - {refresh_response.text}')
