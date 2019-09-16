
#third party
import pytest

#local
from apollo.auth.base import AuthBase



class MockAPIAuth(AuthBase):
    """My custom API"""

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

@pytest.mark.auth
def test_auth():

    api_auth = MockAPIAuth(
        api_key = '123'
    )

    assert api_auth.param ==  {'my_api_key': '123'}
    assert isinstance(api_auth.auth, tuple)
    assert isinstance(api_auth.header, dict)
    assert isinstance(api_auth, AuthBase)