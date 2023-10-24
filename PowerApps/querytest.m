url='https://org425ee2cf.crm.dynamics.com/api/data/v9.2/crddb_autorowreportinputsessions?$top=10';

% Set the access token
% accessToken = 'MYTOKEN';

% Create the options for the HTTP request
options = weboptions('HeaderFields', {'Authorization' ['Bearer ' accessToken]});

% Send the HTTP GET request
response = webread(url, options);

% Process the response as needed
disp(response);