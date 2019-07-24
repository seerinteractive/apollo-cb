
from collections import namedtuple

CLIENT_BUILDER_CASE_PARAMS = [
    'api',
    'auth',
    'folders',
    'params',
    'headers',
    'threads',
    'sleep_interval'
]

ClientBuilderCase = namedtuple(
    'ClientBuilderCase',
    CLIENT_BUILDER_CASE_PARAMS,
    defaults = (None,) * len(CLIENT_BUILDER_CASE_PARAMS)
)


CLIENT_BUILDER_SCENARIOS = [
    ClientBuilderCase(
        api = 'Harvest',
        folders = 'search',
        params = {
            'q': ['hi', 'there', 'how', 'are', 'you']
        },
        headers = {},
        threads = 2,
        sleep_interval = 0,
    ),
    ClientBuilderCase(
        api = 'MyTest',
        folders = 'search',
        params = {
            'q':['hi', 'there', 'how', 'are', 'you']
        },
        headers = {},
        threads = 2,
        sleep_interval = 0,
    )    
]


CreateURLsCase = namedtuple('CreateURLsCase', 'folders,output')    

CREATE_URLS_SCENARIOS = [
    CreateURLsCase(
        folders = ['hi','there',['how','are']],
        output = ['hi/there/how', 'hi/there/are']
    ),
    CreateURLsCase(
        folders = ['you'],
        output = ['you']
    ),
]


CreateParamsCase = namedtuple('CreateParamsCase', 'params,output')    

CREATE_PARAMS_SCENARIOS = [
    CreateParamsCase(
        params = {'a':[1,2]},
        output = [{'a': 1}, {'a': 2}]
    ),
    CreateParamsCase(
        params = {'b':[3,4,'hi']},
        output = [{'b': 3}, {'b': 4}, {'b': 'hi'}]
    ),
]

BuildRequestCase = namedtuple('BuildRequestCase', 'base_url,folders,params,headers')    

BUILD_REQUEST_SCENARIOS = [
    BuildRequestCase(
        base_url = 'http://www.google.com',
        folders = ['search',['this','page']],
        params = {'a':[1,'2']},
        headers = {'i_am':'a header'}
    ),    
]