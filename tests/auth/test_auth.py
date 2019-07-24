import pytest

from apollo import Auth
from tests.data.auth_data import TEST_AUTH_SCENARIOS

@pytest.mark.parametrize('case',TEST_AUTH_SCENARIOS)
@pytest.mark.auth
def test_auth(case):

    a = Auth(
        case.api,
        case.request_headers,
        case.request_auth,
        *case.auth,
        **case.params
    )

    assert case.header_response == a.headers
    assert case.param_response == a.params
    assert case.auth_response == a.auth
