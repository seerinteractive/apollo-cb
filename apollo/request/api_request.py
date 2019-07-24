import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from pprint import pprint as p

class APIRequest:
    '''
    Made b/c need request object before it is made
    '''
    def __init__(self,
                 method,
                 url,
                 params,
                 headers,
                 auth,
                 data,
                 file_pattern,
                 mod_response,
                 storage,
                 verbose=False
                 ):
        self._method = method
        self._url = url
        self._params = params
        self._headers = headers
        self._response = None        
        self._data = data
        self._storage = storage                 
        self._mod_response = mod_response
        self._file_pattern = file_pattern
        self._verbose = verbose
        self._file_path = self._file_pattern.file_func(self,
            **self._file_pattern.pattern_params
        )
        
        self.__auth = auth #not accessable outside class


    def __repr__(self,):
        return f'APIRequest(method={self.method},url={self.url})'

    @property
    def method(self):     
        return self._method
    @property
    def verbose(self):     
        return self._verbose

    @property
    def storage(self):     
        return self._storage        

    @property
    def file_path(self): 
        return self._file_path        

    @property
    def data(self):
        return self._data

    @property
    def url(self):
        return self._url

    @property
    def params(self):
        return self._params

    @property
    def headers(self):
        return self._headers

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self,value):
        self._response = value
        return value

    @staticmethod
    def _make_request(self,*args, **kwargs):

        session = requests.Session()
        retry = Retry(connect=20, backoff_factor=1.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)

        return session.request(
            *args, **kwargs
        )

    def request(self,):   

        response = self._make_request(
            self.method,
            self.url,
            data=self.data,
            params=self.params,
            headers=self.headers,
            auth=self.__auth
        ) 

        self.response = self._mod_response(response)

        if self.verbose:
            print(f'Url {self.response.url}, Status {self.response.status_code}')

        return self        

    def save(self,):      

        self.storage.write(
            file_path=self.file_path,
            data=self.response.text
        )

        return self

    def __iter__(self):
        yield {
            'method': self.method,
            'url':self.url,
            'params':self.params,
            'headers':self.headers
        }
