#standard
from pprint import pprint as p

#third party
import pytest

#local
from apollo.request.attributes import Url
from apollo.request.factory import RequestFactory
from apollo.request.api_request import APIRequest

from tests.data.request_builder_data import REQUEST_BUILDER_SAFE_SCENARIOS
from tests.data.request_builder_data import REQUEST_BUILDER_ERROR_SCENARIOS


@pytest.mark.parametrize('case',REQUEST_BUILDER_SAFE_SCENARIOS)
@pytest.mark.request_builder_safe
@pytest.mark.request_builder
def test_request_builder_safe(case):

    rb = RequestFactory(
        method = case.method,
        url = case.url,
        param = case.param,
        header = case.header,
        auth = case.auth,
        req_data = case.data,
    )

    assert rb.method == case.method
    for api_request in rb:
        assert isinstance(api_request,APIRequest)
 

@pytest.mark.parametrize('case',REQUEST_BUILDER_ERROR_SCENARIOS)
@pytest.mark.request_builder_error
@pytest.mark.request_builder
def test_request_builder_error(case):


    with pytest.raises(case.expected):

        rb = RequestFactory(
            method = case.method,
            url = case.url,
            param = case.param,
            header = case.header,
            auth = case.auth,
            req_data = case.data,
        )
        rb.method
        rb.url
        rb.param
        rb.header
        rb.auth
        rb.req_data




















