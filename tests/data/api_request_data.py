from collections import namedtuple

from tests.mocks.google_cloud import MockStorage
from tests.mocks.api_request import mock_file_pattern
from apollo.utils import FilePath

#api request cases

API_REQUEST_CASE_PARAMS = [
    'method',
    'url',
    'params',
    'headers',
    'auth',
    'data',
    'storage',
    'file_pattern',
    'mod_response',
]

APIRequestCase = namedtuple(
    'APIRequestCase',
    API_REQUEST_CASE_PARAMS,
    defaults = (None,) * len(API_REQUEST_CASE_PARAMS)
)

TEST_API_REQUEST_SCENARIOS = [
    APIRequestCase(
       method="GET", 
       url='http://www.google.com', 
       params={'my_param': 'file_one'}, 
       headers={'my_header': 'headers_val'},
       data={'my': 'data'},
       storage=MockStorage(),
       file_pattern=FilePath(
           mock_file_pattern,
           {'date':'2018/01/01'}
        ),
        mod_response = lambda x: x
    ),
    APIRequestCase(
       method="GET", 
       url='http://www.cnn.com', 
       params={'my_param': 'file_two'}, 
       headers={'my_header': 'headers_val'},
       data={'my': 'data'},
       storage=MockStorage(),
       file_pattern=FilePath(
           mock_file_pattern,
           {'date': '2015/11/01'}
        ),
        mod_response = lambda x: x,
    )
]

#response cases

RespCase = namedtuple(
    'RespCase',
    'file_path, url',
)


TEST_RESP_SCENARIOS = [
    RespCase(
       file_path = '2018/01/01/file_one.json',
       url = 'http://www.google.com',
    ),
    RespCase(
       file_path='2015/11/01/file_two.json',
       url = 'http://www.cnn.com',
    ),
]

