% Set the authentication parameters
clientId = '673d9e85-b0d1-4f5a-ae7a-3dccf0c31a9f';
clientSecret = 'Fo38Q~tcNdLNzs5rPl5.W6.-fCLubnFIK4v3Vdb.';
tenantId = 'ec359ba1-630b-4d2b-b833-c8e6d48f8059';
scope = 'https://org425ee2cf.crm.dynamics.com/.default';

tokenUrl = ['https://login.microsoftonline.com/' tenantId '/oauth2/v2.0/token'];

% Set the request data
data = ['grant_type=client_credentials', ...
        '&client_id=', clientId, ...
        '&client_secret=', clientSecret, ...
        '&scope=', scope];

% Send the request to obtain the access token
% options = weboptions('RequestMethod', 'post');
options=weboptions('HeaderFields',{'Content-Type' 'application/x-www-form-urlencoded'}) ;
response = webwrite(tokenUrl, data, options);
accessToken = response.access_token

% Use the access token to make requests to the Power Platform APIs
% You can include the access token in the Authorization header of your requests

% % Example: Get the list of tables in your environment
% apiUrl = 'https://org425ee2cf.api.crm.dynamics.com/api/data/v9.1/EntityDefinitions';
% headers = struct('Authorization', ['Bearer ', accessToken]);
% response = webread(apiUrl, weboptions('HeaderFields', headers));
% 
% % Display the response
% disp(response);
