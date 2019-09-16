#standard
from pprint import pprint as p

#third party
import pytest

#local
from apollo.auth import Pipedrive
from apollo.builder.client import ApolloCB

from apollo.utils import RateLimit

from apollo.storage.base import StorageBase
from apollo.utils import FilePattern

from apollo.request.attributes import Url
from apollo.request.attributes import Param
from apollo.request.attributes import Header
from apollo.request.attributes import Auth
from apollo.request.attributes import Data
from apollo.request.attributes import Cookie

from apollo.auth.base import AuthBase

from apollo.request import APIRequest


@pytest.mark.client_builder
def test_client_builder():

    #create an api client
    class MyAPI(AuthBase):
        def __init__(
            self,
            api_key
        ):
            self._api_key = api_key
        @property
        def param(self):
            return {
                'my_api_key': self._api_key
            }

    api_auth = MyAPI(
        api_key = '123'
    )

    #create a storage client
    class MyStorage(StorageBase):
        
        def write(self, file_path, data):
            #save data somewhere
            pass

    storage = MyStorage()

    #generate the urls and params for the requests
    URL_LIMIT = 20

    url = Url(
        path_format = "http://httpbin.org/anything/{a}/{b}",
        a = [f'folder{n}' for n in range(URL_LIMIT)],
        b = [f'subfolder{n}' for n in range(URL_LIMIT)]
    )

    param = Param(
        static = {'param_a': 'a'},
        dynamic = {'b': [n for n in range(URL_LIMIT)]}
    )
    
    #set the rate limits
    api_rate_limit = RateLimit(
        rate = 5,
        limit = 5
    )

    storage_rate_limit = RateLimit(
        rate = 1,
        limit = 1
    )

    #modify the response before storage
    def mod_response(response):
        #remove the api key from the json response
        del response.json['args']['my_api_key']
        return response

    
    #stop crawling after 10 responses
    def stop_criteria(response):
        if int(response.json['args']['b']) >= 10:
            return True
    
    #create a file pattern using the response
    def file_func(self, custom_param):
        json = self.response.json
        return f"{json['method']}/{json['args']['b']}/{custom_param}"

    file_pattern = FilePattern(
        file_func = file_func,
        custom_param = 'there'
    )

    rf = ApolloCB(
        method = "GET", 
        url = url,
        param = param,
        api_auth = api_auth,        
        verbose = True,
        save = True,
        file_pattern = file_pattern,
        api_rate_limit = api_rate_limit,   
        stop_criteria = stop_criteria,
        storage = storage,
        mod_response = mod_response,
        storage_rate_limit = storage_rate_limit,
    )

    a = rf.execute()
    for b in a:
        isinstance(b, APIRequest)


# [08:23:10] Url http://httpbin.org/anything/folder0/subfolder0?b=0&param_a=a&my_api_key=123, Status 200
# [08:23:10] Url http://httpbin.org/anything/folder3/subfolder3?b=3&param_a=a&my_api_key=123, Status 200
# [08:23:10] Url http://httpbin.org/anything/folder2/subfolder2?b=2&param_a=a&my_api_key=123, Status 200
# [08:23:10] Url http://httpbin.org/anything/folder1/subfolder1?b=1&param_a=a&my_api_key=123, Status 200
# [08:23:10] Url http://httpbin.org/anything/folder4/subfolder4?b=4&param_a=a&my_api_key=123, Status 200
# [08:23:10] Filepath GET/0/there was saved
# [08:23:11] Filepath GET/3/there was saved
# [08:23:12] Filepath GET/2/there was saved
# [08:23:13] Filepath GET/1/there was saved
# [08:23:14] Filepath GET/4/there was saved
# [08:23:15] Filepath GET/9/there was saved
# [08:23:15] Url http://httpbin.org/anything/folder9/subfolder9?b=9&param_a=a&my_api_key=123, Status 200
# [08:23:15] Url http://httpbin.org/anything/folder5/subfolder5?b=5&param_a=a&my_api_key=123, Status 200
# [08:23:15] Url http://httpbin.org/anything/folder6/subfolder6?b=6&param_a=a&my_api_key=123, Status 200
# [08:23:15] Url http://httpbin.org/anything/folder8/subfolder8?b=8&param_a=a&my_api_key=123, Status 200
# [08:23:15] Url http://httpbin.org/anything/folder7/subfolder7?b=7&param_a=a&my_api_key=123, Status 200
# [08:23:16] Filepath GET/5/there was saved
# [08:23:17] Filepath GET/6/there was saved
# [08:23:18] Filepath GET/8/there was saved
# [08:23:19] Filepath GET/7/there was saved