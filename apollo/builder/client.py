# standard library
import asyncio
import itertools
from time import sleep
from pprint import pprint as p
from concurrent.futures import FIRST_EXCEPTION
import types
import logging

# third party
from aiohttp import ClientSession
import async_timeout

import attr
from attr.validators import instance_of
from attr.validators import in_

# local
from apollo.utils import FilePattern
from apollo.utils import RateLimit
from apollo.utils.helpers import HttpAcceptedTypes

from apollo.request.api_request import APIRequest
from apollo.request.factory import RequestFactory

from apollo.storage.base import StorageBase

from apollo.request.attributes import Param
from apollo.request.attributes import Header
from apollo.request.attributes import Auth
from apollo.request.attributes import Data
from apollo.request.attributes import Cookie
from apollo.request.attributes import Url

from apollo.auth.base import AuthBase
from apollo.storage.base import StorageBase

from apollo.builder.exceptions import WrongDataType
from apollo.utils.helpers import zip_longest_ffill
from apollo.utils.helpers import HttpAcceptedTypes


LOGGER_FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=LOGGER_FORMAT, datefmt='[%H:%M:%S]')
log = logging.getLogger()
log.setLevel(logging.INFO)

FETCH_TIMEOUT = 10

@attr.s
class ApolloCB:
    """ApolloCB builds and makes API calls.    

    **Example Usage**
    
    Below we implemented RateLimiting, Storage, FilePattern, 
    Request Attributes and Authorization.
    
    .. code-block:: python

        #local
        from apollo.builder.client import ApolloCB

        from apollo.utils import RateLimit

        from apollo.storage.base import StorageBase
        from apollo.utils import FilePattern

        from apollo.request.attributes import Url
        from apollo.request.attributes import Param
        from apollo.request.attributes import Header
        from apollo.request.attributes import Auth
        from apollo.request.attributes import Data
        from apollo.request.attributes import Cookie

        from apollo.auth.base import AuthBase

        #create an api client
        class MyAPI(AuthBase):
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

        api_auth = MyAPI(
        api_key = '123'
        )

        #create a storage client
        class MyStorage(StorageBase):

        def write(self, file_path, data):
            #save data somewhere
            pass

        storage = MyStorage()

        #generate the urls and params for the requests
        URL_LIMIT = 20

        url = Url(
        path_format = "http://httpbin.org/anything/{a}/{b}",
        a = [f'folder{n}' for n in range(URL_LIMIT)],
        b = [f'subfolder{n}' for n in range(URL_LIMIT)]
        )

        param = Param(
        static = {'param_a': 'a'},
        dynamic = {'b': [n for n in range(URL_LIMIT)]}
        )

        #set the rate limits
        api_rate_limit = RateLimit(
        rate = 5,
        limit = 5
        )

        storage_rate_limit = RateLimit(
        rate = 1,
        limit = 1
        )

        #modify the response before storage
        def mod_response(response):
        #remove the api key from the json response
        del response.json['args']['my_api_key']
        return response

        #stop crawling after 10 responses
        def stop_criteria(response):
        if int(response.json['args']['b']) >= 10:
            return True

        #create a file pattern using the response
        def file_func(self, custom_param):
        json = self.response.json
        return f"{json['method']}/{json['args']['b']}/there"

        file_pattern = FilePattern(
        file_func = file_func,
        custom_param = 'there'
        )

        rf = ApolloCB(
        method = "GET", 
        url = url,
        param = param,
        api_auth = api_auth,        
        verbose = True,
        save = True,
        file_pattern = file_pattern,
        api_rate_limit = api_rate_limit,   
        stop_criteria = stop_criteria,
        storage = storage,
        mod_response = mod_response,
        storage_rate_limit = storage_rate_limit,
        )

        a = rf.execute()

    :type method: str
    :param method: Options are valid Rest calls, e.g. GET, POST, PUT, DELETE, etc.    

    :type url: :class:`~apollo.request.attributes.Url`
    :param url: List of Urls to request.

    :type param: :class:`~apollo.request.attributes.Param`
    :param param: List of params included in request.

    :type header: :class:`~apollo.request.attributes.Header`
    :param header: List of headers included in request.

    :type auth: :class:`~apollo.request.attributes.Auth`
    :param auth: List of auths included in request.

    :type data: :class:`~apollo.request.attributes.Data`
    :param data: List of data included in request.

    :type cookie: :class:`~apollo.request.attributes.Cookie`
    :param cookie: List of cookies included in request.

    :type api_auth: :class:`~apollo.auth.base.AuthBase`
    :param api_auth: Class that inherits from AuthBase.

    :type zip_type: `zip <https://docs.python.org/3.3/library/functions.html#zip>`_-like function
    :param zip_type: Default is :func:`~apollo.utils.helpers.zip_longest_ffill`.

    :type file_pattern: :class: `~apollo.utils.helpers.FilePattern`
    :param file_pattern: The FilePattern object that will create the file pattern, only used if storing data.

    :type mod_response: lambda
    :param mod_response: Any function that will manipulate and return :class:`~apollo.request.Response`

    :type storage: :class:`~apollo.storage.base.StorageBase`
    :param storage: Any object that inherits from :class:`~apollo.storage.base.StorageBase` and implements a `write(self, file_path, data)` method.

    :type verbose: boolean
    :param verbose: Set True if you'd like logging enabled. This is useful for development.

    :type stop_criteria: lambda
    :param stop_criteria: Any function that will manipulate :class:`~apollo.request.Response` and return True or False.

    :type storage_criteria: lambda
    :param storage_criteria: Any function that accepts :class:`~apollo.request.APIRequest` and return True or False.

    :type save: boolean
    :param save: Saves the :class:`~apollo.request.APIRequest` objects to memory for use after execution.

    :type api_rate_limit: :class:`~apollo.utils.RateLimit`
    :param api_rate_limit: Rate limiting for API calls.

    :type storage_rate_limit: :class:`~apollo.utils.RateLimit`
    :param storage_rate_limit: Rate limiting for storage.



    """
    # request builder
    url = attr.ib(instance_of(Url))
    method = attr.ib(default = 'GET', validator = in_(HttpAcceptedTypes.ACCEPTED_METHODS))
    param = attr.ib(default = Param(), validator = instance_of(Param))
    header = attr.ib(default = Header(), validator = instance_of(Header))
    auth = attr.ib(default = Auth(), validator = instance_of(Auth))
    data = attr.ib(default = Data(), validator = instance_of(Data))
    cookie = attr.ib(default = Cookie(), validator = instance_of(Cookie))
    api_auth = attr.ib(default = AuthBase(), validator = instance_of(AuthBase))
    zip_type = attr.ib(default = zip_longest_ffill, validator = instance_of(types.FunctionType))
    file_pattern = attr.ib(default = FilePattern(), validator = instance_of(FilePattern))
    mod_response = attr.ib(default = lambda x: x, validator = instance_of(types.FunctionType))
    storage = attr.ib(default = None, validator = instance_of((StorageBase, type(None))))
    verbose = attr.ib(default = False, validator = instance_of(bool))
    # content_type = attr.ib(default = 'json', validator = in_(HttpAcceptedTypes.ACCEPTED_CONTENT_TYPES))

    # clientbuilder specific
    stop_criteria = attr.ib(default = lambda x: x, validator = instance_of(types.FunctionType))
    storage_criteria = attr.ib(default = lambda x: x, validator = instance_of(types.FunctionType))
    save = attr.ib(default = False, validator = instance_of(bool))
    api_rate_limit = attr.ib(default = RateLimit(), validator = instance_of(RateLimit))
    storage_rate_limit = attr.ib(default = RateLimit(), validator = instance_of(RateLimit))

    def _build_requests(self):
        """
        Implements a RequestFactory to create APIRequests.

        :returns: generator
        """

        rf = RequestFactory(
            method = self.method,
            url = self.url,
            param = self.param,
            header = self.header,
            auth = self.auth,
            req_data = self.data,
            cookie = self.cookie,
            zip_type = self.zip_type,
            file_pattern = self.file_pattern,
            mod_response = self.mod_response,
            storage = self.storage,
            verbose = self.verbose,
        )

        if self.verbose:
            log.info(f"{len(rf)} requests built.")

        for req in rf:
            auth_req = self.api_auth >> req
            yield auth_req

    async def add_requests(self, requests):
        """
        Executes and executes :func:`~apollo.request.APIRequest.request` and :func:`~apollo.request.APIRequest.save` methods on :class:`~apollo.request.APIRequest` objects.
        """

        api_semaphore = asyncio.Semaphore(self.api_rate_limit.limit)
        storage_semaphore = asyncio.Semaphore(self.storage_rate_limit.limit)

        tasks = []

        for request in requests:
            tasks.append(
                asyncio.ensure_future(
                    request.request(
                        api_rate_limit=self.api_rate_limit.limit,
                        storage_rate_limit=self.storage_rate_limit.limit,
                        api_semaphore=api_semaphore,
                        storage_semaphore=storage_semaphore,
                        stop_criteria=self.stop_criteria,
                    )
                )
            )

        tasks = {key: n for n, key in enumerate(tasks)}

        done, pending = await asyncio.wait(tasks.keys(), return_when=FIRST_EXCEPTION)

        for pending_task in pending:
            pending_task.cancel()

        completed_tasks = []

        for task in done:
            try:
                completed_tasks.append(task.result())
            except Exception:
                pass

        return completed_tasks

    def execute(self,):
        """
        Executes the request. 
        
        :returns: None or if ``save`` is set to ``True``, the return will be a list of :func:`~apollo.request.APIRequest`.

        """
        if self.verbose:
            log.info("Building requests")

        requests = self._build_requests()

        responses = asyncio.run(self.add_requests(requests=requests))

        if self.verbose:
            log.info(f"Responses received: {len(responses)}")

        if self.save:
            return responses
