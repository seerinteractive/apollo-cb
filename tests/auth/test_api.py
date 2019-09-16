#standard
from pprint import pprint as p
import os

#third party
import pytest

#local
from apollo.auth import Pipedrive
from apollo.auth import BambooHR
from apollo.auth import Harvest

from apollo.utils import RateLimit

from apollo.builder.client import ApolloCB

from apollo.request import attributes as attrib

API_RATE_LIMIT = RateLimit(rate = 1, limit = 1)

@pytest.mark.api
@pytest.mark.bamboohr
def test_bamboohr():

    BAMBOOHR_API_KEY = os.environ.get('BAMBOOHR_API_KEY', '123')
    BAMBOOHR_SUBDOMAIN = os.environ.get('BAMBOOHR_SUBDOMAIN', '123')

    api_auth = BambooHR(
        api_key = BAMBOOHR_API_KEY,
        subdomain = BAMBOOHR_SUBDOMAIN,
    )

    url = attrib.Url(
        path_format = f'{api_auth.base}/employees/directory'
    )

    cb = ApolloCB(
        method = 'GET',
        url = url,
        api_auth = api_auth,
        api_rate_limit = API_RATE_LIMIT,
        save = True,
        verbose = True,
    )

    a, *_ = cb.execute()

    assert a.response.status == 200

@pytest.mark.api
@pytest.mark.pipedrive
def test_pipedrive():

    PIPEDRIVE_API_KEY = os.environ.get('PIPEDRIVE_API_KEY','123')

    api_auth = Pipedrive(
        api_key = PIPEDRIVE_API_KEY
    )

    url = attrib.Url(
        path_format = f'{api_auth.base}/pipelines'
    )

    cb = ApolloCB(
        method = 'GET',
        url = url,
        api_auth = api_auth,
        api_rate_limit = API_RATE_LIMIT,
        save = True,
        verbose = True,
    )

    a, *_ = cb.execute()

    assert a.response.status == 200

@pytest.mark.api
@pytest.mark.harvest
def test_harvest():
    
    HARVEST_ACCOUNT_ID = os.environ.get('HARVEST_ACCOUNT_ID','123')
    HARVEST_ACCESS_TOKEN = os.environ.get('HARVEST_ACCESS_TOKEN','123')

    api_auth = Harvest(
        account_id = HARVEST_ACCOUNT_ID,
        access_token = HARVEST_ACCESS_TOKEN,
        user_agent = 'My App'
    )

    url = attrib.Url(
        path_format = f'{api_auth.base}/users'
    )

    cb = ApolloCB(
        method = 'GET',
        url = url,
        api_auth = api_auth,
        api_rate_limit = API_RATE_LIMIT,
        save = True,
        verbose = True,
    )

    a, *_ = cb.execute()

    assert a.response.status == 200


