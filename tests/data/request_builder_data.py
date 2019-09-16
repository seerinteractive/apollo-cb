from collections import namedtuple

from apollo.builder.exceptions import MethodError
from apollo.builder.exceptions import NestedFoldersForbidden
from apollo.builder.exceptions import ListAsValueRequired
from apollo.builder.exceptions import MoreThanOneKeySupplied
from apollo.builder.exceptions import OnlyStringsOrIntsAllow
from apollo.builder.exceptions import DelimiterMustBeString


from apollo.request.attributes import Param
from apollo.request.attributes import Url
from apollo.request.attributes import Header
from apollo.request.attributes import Auth
from apollo.request.attributes import Data

import pytest


DictConv = namedtuple('DictConv','static,dynamic,expected')

DICT_CONVERTER_SAFE_SCENARIOS = [
    DictConv(
        static = {'a': 1},
        dynamic = {'b': [2 , 3]},
        expected = [{'b': 2, 'a': 1}, {'b': 3, 'a': 1}]
    ),
        DictConv(
        static = {'a': 1},
        dynamic = {'b': [2 , 3]},
        expected = [{'b': 2, 'a': 1}, {'b': 3, 'a': 1}]
    ),
        DictConv(
        static = {'a': 1},
        dynamic = {},
        expected = [{'a': 1}]
    ),
    DictConv(
        static = {},
        dynamic = {'a': [1, 2]},
        expected = [{'a': 1}, {'a': 2}]
    ),
]

DICT_CONVERTER_ERROR_SCENARIOS = [
    #dynamic
    DictConv(
        static = {'a': 1},
        dynamic = {'b': [1,2], 'c':[1]},
        expected = MoreThanOneKeySupplied,
    ),    
    DictConv(
        static = {'b': 1},
        dynamic = {'a': 1},
        expected = ListAsValueRequired,
    ),
    #static
    DictConv(
        static = {'b': [2 , 3]},
        dynamic = {'a': [1, 2]},
        expected = OnlyStringsOrIntsAllow,
    ),
]

ListConv = namedtuple('ListConv','static,dynamic,delimiter,expected')

LIST_CONVERTER_SAFE_SCENARIOS = [
    ListConv(
        static = [1, 2],
        dynamic = [3, 4],
        delimiter = '',
        expected = ['1/2/3', '1/2/4']
    ),
   ListConv(
        static = [],
        dynamic = [3, 4],
        delimiter = '/',
        expected = ['3', '4']
    ),    
   ListConv(
        static = [1, 2],
        dynamic = [],
        delimiter = '.',
        expected = ['1.2']
    ), 
   ListConv(
        static = '1',
        dynamic = [],
        delimiter = '.',
        expected = ['1']
    ),     

]

LIST_CONVERTER_ERROR_SCENARIOS = [
    ListConv(
        static = [1, 2, [1,2]],
        dynamic = [3, 4],
        delimiter = None,
        expected = NestedFoldersForbidden
    ),
    ListConv(
        static = [3, 4],
        dynamic = [1, 2, [1,2]],
        delimiter = None,
        expected = NestedFoldersForbidden
    )           
]


REQUEST_BUILDER_FIELDS = [
    'method',
    'url',
    'param',
    'header',
    'auth',
    'data',
    'zip_type',
    'expected'
]

RequestBuilderCase = namedtuple('RequestBuilderCase', REQUEST_BUILDER_FIELDS)

REQUEST_BUILDER_SAFE_SCENARIOS = [
    RequestBuilderCase(
        method = 'GET',
        url = Url(
            path_format = "http://httpbin.org/{a}/{b}/{c}", 
            a='anything', b='last', c = ['it', 'is']
        ),
        param = Param(
            dynamic = {'a':[1,2]}
        ),
        header = Header(
            dynamic = {'b': [3, 4, 5]}
        ), 
        auth = Auth(),
        data = Data(),
        zip_type = None,
        expected = None
    ),
]

REQUEST_BUILDER_ERROR_SCENARIOS = [
    #incorect method
    RequestBuilderCase(
        method = 'LMNOP',
        url = Url(
            path_format='https://httpbin.org'
        ),
        param = Param(
            dynamic = {'a':[1,2]}
        ),
        header = Header(
            dynamic = {'b': [3, 4, 5]}
        ), 
        auth = Auth(),
        data = Data(),
        zip_type = None,
        expected = ValueError
    ),
    RequestBuilderCase(
        method = 'GET',
        url = 1,
        param = Param(
            dynamic = {'a':[1,2]}
        ),
        header = Header(
            dynamic = {'b': [3, 4, 5]}
        ), 
        auth = Auth(),
        data = Data(),
        zip_type = None,
        expected = TypeError
    ),  
    RequestBuilderCase(
        method = 'GET',
        url = Url(
            path_format='https://httpbin.org'
        ),
        param = "I shouldn't be here",
        header = Header(
            dynamic = {'b': [3, 4, 5]}
        ), 
        auth = Auth(),
        data = Data(),
        zip_type = None,
        expected = TypeError
    ),  
    RequestBuilderCase(
        method = 'GET',
        url = Url(
            path_format='https://httpbin.org'
        ),
        param = Param(
            dynamic = {'a':[1,2]}
        ),
        header = "I shouldn't be here.",
        auth = Auth(),
        data = Data(),
        zip_type = None,
        expected = TypeError
    ), 
    RequestBuilderCase(
        method = 'GET',
        url = Url(
            path_format='https://httpbin.org'
        ),
        param = Param(
            dynamic = {'a':[1,2]}
        ),
        header = Header(),
        auth = Header(),
        data = Data(),
        zip_type = None,
        expected = TypeError
    ), 
    RequestBuilderCase(
        method = 'GET',
        url = Url(
            path_format='https://httpbin.org'
        ),
        param = Param(
            dynamic = {'a':[1,2]}
        ),
        header = Header(),
        auth = Header(),
        data = Header(),
        zip_type = None,
        expected = TypeError
    ),                  
]