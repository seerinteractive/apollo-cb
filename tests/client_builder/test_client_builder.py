import pytest

from pprint import pprint as p

from apollo import Auth
from apollo import APIRequest
from apollo import ClientBuilder

from tests.data.client_builder_data import CLIENT_BUILDER_SCENARIOS
from tests.data.client_builder_data import CREATE_URLS_SCENARIOS

from tests.data.client_builder_data import CREATE_PARAMS_SCENARIOS
from tests.data.client_builder_data import BUILD_REQUEST_SCENARIOS

from tests.data.auth_data import TEST_AUTH_SCENARIOS

TEST_CLIENT_BUILDER_SCENARIOS = list(
    zip(
        TEST_AUTH_SCENARIOS,
        CLIENT_BUILDER_SCENARIOS,
    )
)


@pytest.mark.client_builder
@pytest.mark.parametrize('auth_case,client_builder_case',TEST_CLIENT_BUILDER_SCENARIOS)
@pytest.mark.client_builder_attr
def test_client_builder_attr(auth_case,client_builder_case):

    auth = Auth(
        auth_case.api,
        auth_case.request_headers,
        auth_case.request_auth,
        *auth_case.auth,
        **auth_case.params
    )
    case = client_builder_case._replace(auth = auth)

    c = ClientBuilder(**case._asdict())

    assert case.api == c.api
    assert isinstance(case.auth, Auth)
    assert case.folders == c.folders
    assert case.params == c.params
    assert case.headers == c.headers
    assert case.threads == c.threads
    assert case.sleep_interval == c.sleep_interval



@pytest.mark.client_builder
@pytest.mark.client_builder_create_urls
@pytest.mark.parametrize('case',CREATE_URLS_SCENARIOS)
def test_client_builder_create_urls(case):

    c = ClientBuilder.create_urls(*case.folders)
    assert case.output == list(c)




@pytest.mark.client_builder
@pytest.mark.client_builder_create_params
@pytest.mark.parametrize('case',CREATE_PARAMS_SCENARIOS)
def test_client_builder_create_params(case):

    c = ClientBuilder.create_params(**case.params)
    assert case.output == list(c)


@pytest.mark.client_builder
@pytest.mark.client_builder_build_request
@pytest.mark.parametrize('case',BUILD_REQUEST_SCENARIOS)
def test_client_builder_build_request(case):

    c = ClientBuilder._build_request(**case._asdict())
    for api_request in list(c):
        assert isinstance(api_request,APIRequest)

