#standard
from pprint import pprint as p
import types

#third party
import pytest

#local
from apollo.request import Response
from apollo.request import APIRequest

from apollo.utils.helpers import FilePattern

from apollo.storage.base import StorageBase

@pytest.mark.api_request
def test_api_request():
    
    URL = 'myurl.com'
    
    req = APIRequest(
        url = URL
    )

    assert req.url == URL

    #check defaultss
    assert req.method == 'GET'
    assert isinstance(req.param, dict)
    assert isinstance(req.header, dict)
    assert isinstance(req.auth, type(None))
    assert isinstance(req.data, dict)
    assert isinstance(req.cookie, dict)
    assert isinstance(req.file_pattern, type(None))
    assert isinstance(req.mod_response, types.FunctionType)
    assert isinstance(req.storage, type(None))
    assert isinstance(req.storage_criteria, types.FunctionType)
    assert isinstance(req.mod_response, types.FunctionType)
    assert isinstance(req.verbose, bool)
    assert isinstance(req.response, Response)
    
    

