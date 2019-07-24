
_ENDPOINTS = {
    'Harvest': 'https://api.harvestapp.com/v2',
    'BambooHR': 'https://api.bamboohr.com/api/gateway.php',
    'Pipedrive': 'https://api.pipedrive.com/v1'

}

_REQUEST_HEADERS = {
    'Harvest': lambda access_token, account_id:
    {
        "Authorization": f"Bearer {access_token}",
        "Harvest-Account-Id": account_id,
        "User-Agent": "Apollo-CB"
    },
    'BambooHR': lambda x: {'Accept': 'application/json'},
    'Pipedrive': lambda x: {
        "Accept": "application/json, */*", 
        "content-type": "application/json",
        "User-Agent": "Apollo-CB"
    }
}

_REQUEST_AUTH = {
    'BambooHR': lambda api_key: (api_key, '')
}

class Auth:

    def __init__(
        self,
        api,
        request_headers = _REQUEST_HEADERS,
        request_auth = _REQUEST_AUTH,
        *auth,
        **params
    ):
        self._api = api
        self._auth = auth or [None]
        self._params = params or {}
        self._request_headers = request_headers
        self._request_auth = request_auth

    @property
    def headers(self,):

        try:
            return self._request_headers[self._api](*self._auth)
        except Exception as e:
            print(e)
            return {}

    @property
    def auth(self,):
        try:
            return self._request_auth[self._api](*self._auth)
        except Exception as e:
            return ()
        
    
    @property
    def params(self,):
        return self._params