import pytest

from requests import Request

from unittest import mock

from apollo import APIRequest
from apollo.utils import FilePath
from tests.mocks.google_cloud import MockStorage

from tests.data.auth_data import TEST_AUTH_SCENARIOS
from tests.data.api_request_data import TEST_API_REQUEST_SCENARIOS
from tests.data.api_request_data import TEST_RESP_SCENARIOS

from pprint import pprint as p

TEST_API_REQUEST_SCENARIOS_ZIP = list(
    zip(
        TEST_AUTH_SCENARIOS,
        TEST_API_REQUEST_SCENARIOS,
        TEST_RESP_SCENARIOS
    )
)

@pytest.mark.api_request
@pytest.mark.api_request_attrib
@pytest.mark.parametrize('auth_case,api_case,resp_case',TEST_API_REQUEST_SCENARIOS_ZIP)
def test_api_request_attrib(auth_case,api_case,resp_case):

    req_case = api_case._replace(auth = auth_case)
    req = APIRequest(**req_case._asdict())

    assert req.method == req_case.method
    assert req.url == req_case.url
    assert req.params == req_case.params
    assert req.headers == req_case.headers
    assert req.data == req_case.data
    assert isinstance(req.storage,MockStorage)

    assert req.file_path == resp_case.file_path

@pytest.mark.xfail
@pytest.mark.api_request
@pytest.mark.api_request_auth
@pytest.mark.parametrize('auth_case,api_case,resp_case',TEST_API_REQUEST_SCENARIOS_ZIP)
def test_api_request_auth(auth_case,api_case,resp_case):
    
    #all auth should be be able to be accessed
    
    req_case = api_case._replace(auth = auth_case)
    req = APIRequest(**req_case._asdict())
    
    req.auth

@pytest.mark.api_request
@pytest.mark.api_request_make
@pytest.mark.parametrize('auth_case,api_case,resp_case',TEST_API_REQUEST_SCENARIOS_ZIP)
def test_api_request_make(auth_case,api_case,resp_case):
    
    req_case = api_case._replace(auth = auth_case)
    req = APIRequest(**req_case._asdict())
    
    req._make_request = Request
    resp = req.request()
    assert resp.response.url == resp_case.url


@pytest.mark.api_request
@pytest.mark.api_request_save
@pytest.mark.parametrize('auth_case,api_case,resp_case',TEST_API_REQUEST_SCENARIOS_ZIP)
def test_api_request_save(auth_case,api_case,resp_case):
    
    req_case = api_case._replace(auth = auth_case)
    req = APIRequest(**req_case._asdict())

    req._make_request = Request
    resp = req.request()
    resp.response.text = 'dummy' #.save() requires the requests obj to contain .text

    assert isinstance(resp.save(),APIRequest)
