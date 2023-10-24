
% Define the necessary parameters
url = 'https://org425ee2cf.api.crm.dynamics.com';
clientId = '51f81489-12ee-4a9e-aaae-a2591f45987d';
% clientId = '673d9e85-b0d1-4f5a-ae7a-3dccf0c31a9f';
callbackBaseUrl = 'https://localhost';

% Construct the authorization URL with query parameters
authUrl = [...
    'https://login.microsoftonline.com/common/oauth2/authorize?'...
    'client_id=' clientId '&response_type=code&redirect_uri=' callbackBaseUrl '&resource=' url];

% Open the authorization URL in a browser
web(authUrl);

% Wait for the user to complete the authorization and extract the callback URL with the authorization code
callbackUrl = input('Enter the callback URL after completing the authorization: ', 's');

% Parse the authorization code from the callback URL
authorizationCode = extractBetween(callbackUrl, 'code=', '&');

% Exchange the authorization code for an access token
tokenUrl = 'https://login.microsoftonline.com/common/oauth2/token';

opts=weboptions('HeaderFields',{'Content-Type' 'application/x-www-form-urlencoded'}) ;
response = webwrite(tokenUrl, ...
    'grant_type', 'authorization_code',...
    'client_id', clientId,...
    'code',  authorizationCode,...
    'redirect_uri', callbackBaseUrl, opts);

% Extract the access token from the response
accessToken = response.access_token;

% Use the access token for subsequent API requests
% (perform your desired actions with the obtained access token)

% Display the access token
disp('Access token:');
disp(accessToken);

% refresh = webwrite(tokenUrl, ...
%     'grant_type', 'refresh_token',...
%     'client_id', clientId,...
%     'refresh_token',  response.refresh_token,...
%     'redirect_uri', callbackUrl, opts);

