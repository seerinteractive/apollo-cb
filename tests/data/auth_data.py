from collections import namedtuple

request_headers = {
    'MyTest': lambda header_val:
    {
        "Authorization": f"Bearer {header_val}",
        "Account-Id": '867-5301',
        "User-Agent": "Jenny"        
    }
}

request_auth = {
    'MyTest': lambda api_key: (api_key, '')
}

AUTH_CASE_PARAMS = [
    'api', 
    'auth', 
    'request_headers', 
    'request_auth', 
    'params',
    'param_response', 
    'header_response', 
    'auth_response',
]

AuthCase = namedtuple('Auth', AUTH_CASE_PARAMS)

TEST_AUTH_SCENARIOS = [
    AuthCase(
       api = 'MyTest', 
       auth = ['hi'], 
       request_headers = request_headers,
       request_auth = request_auth,
       params = {}, 
       param_response = {}, 
       header_response = {
           'Authorization': 'Bearer hi', 
           'Account-Id': '867-5301', 
           'User-Agent': 'Carl'
        },
       auth_response = ('hi', '')
    ),
    AuthCase(
       api = 'MyTest', 
       auth = ['star'], 
       request_headers = request_headers,
       request_auth = request_auth,
       params = {'carl': 'sagan'}, 
       param_response = {'carl': 'sagan'}, 
       header_response = {
           'Authorization': 'Bearer star', 
           'Account-Id': '867-5301', 
           'User-Agent': 'Jenny'
        },
       auth_response = ('star', '')
    )
]