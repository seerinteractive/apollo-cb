#standard
import asyncio
import logging
from pprint import pprint as p
import types

#third party
import async_timeout
from aiohttp import ClientSession
from aiohttp import BasicAuth
from attr.validators import instance_of

import attr
from attr.validators import in_

#local
from apollo.utils import FilePath
from apollo.utils import FilePattern
from apollo.utils.helpers import HttpAcceptedTypes

from apollo.storage.base import StorageBase

from apollo.request.base import RequestBase

from apollo.builder.exceptions import WrongDataType

LOGGER_FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(format=LOGGER_FORMAT, datefmt="[%H:%M:%S]")
log = logging.getLogger()
log.setLevel(logging.INFO)

FETCH_TIMEOUT = 10

@attr.s
class Response:
    """
    A container for `aiohttp.ClientResponse <https://docs.aiohttp.org/en/stable/client_reference.html#client-session>`_

    We need to save the data associated `aiohttp.ClientRequest <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse>`_ because aiohttp will close the connection (as it's non-blocking). Before the connection is closed, we save the data to this container.

    :type method: str
    :param method: See `aiohttp.ClientRequest.method <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.method>`_

    :type url: str
    :param url: See `aiohttp.ClientRequest.url <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.url>`_

    :type cookies: `http.cookies.SimpleCookie <https://docs.python.org/3/library/http.cookies.html#http.cookies.SimpleCookie>`_
    :param cookies: See `aiohttp.ClientRequest.cookies <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.cookies>`_

    :type status: int
    :param status: See `aiohttp.ClientRequest.status <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.status>`_

    :type json: dict
    :param json: Response from the coroutine here: `aiohttp.ClientRequest.json <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.json>`_

    :type byte_vals: bytes
    :param byte_vals: Response from the coroutine here: `aiohttp.ClientRequest.read <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.read>`_

    :type text: str
    :param text: Response from the coroutine here: `aiohttp.ClientRequest.text <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.text>`_

    :type encoding: str
    :param encoding: See `aiohttp.ClientRequest.get_encoding <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.get_encoding>`_

    :type history: A `Sequence <https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence>`_ of `ClientResponse <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse>`_ objects
    :param history: See `aiohttp.ClientRequest.history <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.history>`_

    :type content_type: str
    :param content_type: See `aiohttp.ClientRequest.content_type <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.content_type>`_

    :type header: `CIMultiDictProxy <https://multidict.readthedocs.io/en/stable/multidict.html#multidict.CIMultiDictProxy>`_
    :param header: See `aiohttp.ClientRequest.header <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.header>`_
    """

    
    method = attr.ib(default = None)
    url = attr.ib(default = None)
    cookies = attr.ib(default = None)
    status = attr.ib(default = None)
    json = attr.ib(default = None)
    byte_vals = attr.ib(default = None)
    text = attr.ib(default = None)
    encoding = attr.ib(default = None)
    history = attr.ib(default = None)
    content_type = attr.ib(default = None)
    header = attr.ib(default = None)
   
@attr.s
class APIRequest:
    """
    API request makes and saves the request.

    :type method: str
    :param method: Options are valid Rest calls, e.g. GET, POST, PUT, DELETE, etc.

    :type url: str 
    :param url: Url being requested.

    :type param: dict
    :param param: Parameters used in request.

    :type header: dict
    :param header: Header used in request.

    :type auth: tuple
    :param auth: Authentication used in request.

    :type data: dict
    :param data: Data used in request.

    :type cookie: dict
    :param cookie: Cookie used in request.

    :type file_pattern: :class:`~apollo.utils.FilePattern`
    :param file_pattern: Pattern the file will be written

    :type mod_response: lambda
    :param mod_response: Accepts and returns a :class:`~apollo.request.Response` object

    :type storage: :class:`~apollo.storage.base.StorageBase`
    :param storage: Any object that inherits from :class:`~apollo.storage.base.StorageBase` and implements a `write(self, file_path, data)` method.

    :type verbose: boolean
    :param verbose: Set True if you'd like logging enabled. This is useful for development.
    """
    
    url = attr.ib(validator = instance_of(str))
    method = attr.ib(default = 'GET', validator = in_(HttpAcceptedTypes.ACCEPTED_METHODS))
    param = attr.ib(default = dict(), validator = instance_of(dict))
    header = attr.ib(default = dict(), validator = instance_of(dict))
    auth = attr.ib(default = None, validator = instance_of((tuple, type(None))), repr = False)
    data = attr.ib(default = dict(), validator = instance_of(dict))
    cookie = attr.ib(default = dict(), validator = instance_of(dict))
    file_pattern = attr.ib(default = None, validator = instance_of((FilePattern, type(None))))
    mod_response = attr.ib(default = lambda x: x, validator = instance_of(types.FunctionType))
    storage = attr.ib(default = None, validator = instance_of((StorageBase, type(None))))
    storage_criteria = attr.ib(default = lambda x: x, validator = instance_of(types.FunctionType))
    mod_response = attr.ib(default = lambda x: x, validator = instance_of(types.FunctionType))
    verbose = attr.ib(default = False, validator = instance_of(bool))
    response = attr.ib(default = Response())

    @property
    def file_path(self):
        """
        File path where the data will be stored. Implements :class:`~apollo.utils.FilePattern`.

        :returns: str
        """
        if self.file_pattern:
            self.file_pattern.lookup_obj = self
            return self.file_pattern.path

    async def request(
        self,
        api_rate_limit,
        storage_rate_limit,
        api_semaphore,
        storage_semaphore,
        stop_criteria,
    ):
        """
        Executes `aiohttp.ClientSession.request <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession.request>`_.
        
        :type api_rate_limit: int
        :param api_rate_limit: The speed with which requests should be executed.
        
        :type storage_rate_limit: int
        :param storage_rate_limit: The speed with which responses should be saved.
        
        :type api_semaphore: int
        :param api_semaphore: Number of requests to be executed at "once"
        
        :type storage_semaphore: int
        :param storage_semaphore: Number of requests to be executed at "once"
        
        :type stop_criteria: lambda
        :param stop_criteria: Any function that will manipulate :class:`~apollo.request.Response` and return True or False.

        :rtype: :class:`~apollo.request.APIRequest`
        :returns: self 
        """
        
        request_args = {
            "method": self.method,
            "url": self.url,
            "params": self.param,
            "data": self.data,
            "cookies": self.cookie,
            "headers": self.header,
        }

        if self.auth:
            request_args.update({"auth": BasicAuth(*self.auth)})

        async with api_semaphore:

            with async_timeout.timeout(FETCH_TIMEOUT):
                async with ClientSession() as session:

                    async with session.request(**request_args) as response:

                        json = await response.json()
                        byte_vals = await response.read()
                        text = await response.text()

                        resp = Response(
                            method=response.method,
                            url=response.url,
                            cookies=response.cookies,
                            status=response.status,
                            json=json,
                            byte_vals=byte_vals,
                            text=text,
                            encoding=response.get_encoding(),
                            history=response.history,
                            content_type=response.content_type,
                            header=response.headers,
                        )

                        stop = stop_criteria(resp)

                        if stop == True:
                            raise Exception

                        self.response = self.mod_response(resp)

                        if self.verbose:
                            log.info(
                                f"Url {self.response.url}, Status {self.response.status}"
                            )

                        if self.storage:

                            asyncio.ensure_future(
                                self.save(
                                    semaphore=storage_semaphore, rate=storage_rate_limit
                                )
                            )

                        await asyncio.sleep(api_rate_limit)

                        return self

    async def save(self, semaphore, rate):
        """
        Saves the response from :meth:`~apollo.request.APIRequest.request`.

        :type semaphore: int
        :param semaphore: Number of requests to be executed at "once"

        :type rate: int
        :param rate: The speed with which responses should be saved.

        :rtype: :class:`~apollo.request.APIRequest`
        :returns: self 
        """
        async with semaphore:
            if self.storage_criteria(self) and self.storage and self.file_path:
                self.storage.write(file_path=self.file_path, data=self.response.text)
                if self.verbose:
                    log.info(f"Filepath {self.file_path} was saved.")
                await asyncio.sleep(rate)
            else:
                pass

            return self
























    # @property
    # def method(self,):
    #     """
    #     aiohttp ClientRequest method. See `aiohttp.ClientRequest.method <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.method>`_

    #     :returns: str
    #     """
    #     return self._method

    # @property
    # def url(self,):
    #     """
    #     aiohttp ClientRequest url. See `aiohttp.ClientRequest.url <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.url>`_

    #     :returns: str
    #     """

    #     return self._url

    # @property
    # def cookies(self,):
    #     """
    #     aiohttp ClientRequest cookie. See `aiohttp.ClientRequest.cookies <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.cookies>`_

    #     :returns: dict
    #     """

    #     return self._cookies

    # @property
    # def status(self,):
    #     """
    #     aiohttp ClientRequest status. See `aiohttp.ClientRequest.status <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.status>`_

    #     :returns: int
    #     """
    #     return self._status

    # @property
    # def json(self,):
    #     """
    #     aiohttp ClientRequest json. Response from the coroutine here: `aiohttp.ClientRequest.json <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.json>`_

    #     :returns: dict
    #     """
    #     return self._json

    # @property
    # def bytes(self,):
    #     """
    #     aiohttp ClientRequest bytes object. Response from the coroutine here: `aiohttp.ClientRequest.read <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.read>`_

    #     :returns: bytes
    #     """
    #     return self._bytes

    # @property
    # def text(self,):
    #     """
    #     aiohttp ClientRequest text. Response from the coroutine here: `aiohttp.ClientRequest.text <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.text>`_

    #     :returns: str
    #     """
    #     return self._text

    # @property
    # def encoding(self,):
    #     """
    #     aiohttp ClientRequest encoding. See `aiohttp.ClientRequest.get_encoding <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.get_encoding>`_

    #     :returns: str
    #     """
    #     return self._encoding

    # @property
    # def history(self,):
    #     """
    #     aiohttp ClientRequest history. See `aiohttp.ClientRequest.history <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.history>`_

    #     :returns: A `Sequence <https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence>`_ of `ClientResponse <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse>`_ objects
    #     """
    #     return self._history

    # @property
    # def content_type(self,):
    #     """
    #     aiohttp ClientRequest content_type. See `aiohttp.ClientRequest.content_type <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.content_type>`_

    #     :returns: str
    #     """
    #     return self._content_type

    # @property
    # def header(self,):
    #     """
    #     aiohttp ClientRequest header. See `aiohttp.ClientRequest.header <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse.header>`_

    #     :returns: `CIMultiDictProxy <https://multidict.readthedocs.io/en/stable/multidict.html#multidict.CIMultiDictProxy>`_
    #     """
    #     return self._header




    #     def __init__(
    #     self,
    #     method,
    #     url,
    #     param,
    #     header,
    #     auth,
    #     data,
    #     cookie,
    #     file_pattern=FilePattern(),
    #     mod_response=lambda x: x,
    #     storage=StorageBase(),
    #     storage_criteria=lambda x: True,
    #     verbose=False,
    # ):

    #     self._method = method
    #     self._url = url
    #     self._param = param
    #     self._header = header
    #     self._data = data
    #     self._cookie = cookie
    #     self._response = Response()        
    #     self._storage = storage
    #     self._storage_criteria = storage_criteria
    #     self._mod_response = mod_response
    #     self._file_pattern = file_pattern
    #     self._verbose = verbose
    #     self._auth = auth or tuple()




    # def __repr__(self,):
    #     return f"APIRequest(method={self.method},url={self.url})"

    # @property
    # def auth(self):
    #     """
    #     Authentication used in request.
        
    #     :returns: tuple
    #     """
    #     if not isinstance(self._auth, tuple):
    #         raise WrongDataType(self._auth, tuple)
    #     return self._auth

    # @auth.setter
    # def auth(self, value):
    #     self._auth = value
    #     return value

    # @property
    # def method(self):
    #     """
    #     Options are valid Rest calls, e.g. GET, POST, PUT, DELETE.

    #     :rtype: str
    #     :returns: GET, POST, PUT or DELETE
    #     """

    #     if self._method not in ['GET', 'POST', 'PUT', 'DELETE']:
    #         raise(f"{self._method} was given but only the following are valid: GET, POST, PUT, DELETE")
    #     return self._method

    # @property
    # def param(self):
    #     """
    #     Parameters used in request.
        
    #     :returns: dict
    #     """
    #     if not isinstance(self._param, dict):
    #         raise WrongDataType(self._param, dict)
    #     return self._param

    # @param.setter
    # def param(self, value):
    #     self._param = value
    #     return value

    # @property
    # def header(self):
    #     """
    #     Headers used in request.
        
    #     :returns: dict
    #     """
    #     if not isinstance(self._header, dict):
    #         raise WrongDataType(self._header, dict)
    #     return self._header        

    # @header.setter
    # def header(self, value):
    #     self._header = value
    #     return value

    # @property
    # def verbose(self):
    #     """
    #     Set True if you'd like logging enabled. This is useful for development.
        
    #     :returns: bool
    #     """
    #     if not isinstance(self._verbose, bool):
    #         raise WrongDataType(self._verbose, bool)
    #     return self._verbose           

    # @property
    # def storage(self):
    #     """
    #     Any object that inherits from :class:`~apollo.storage.base.StorageBase` and implements a :class:`~apollo.storage.base.StorageBase.write` method.

    #     :returns: :class:`~apollo.storage.base.StorageBase`
    #     """        
    #     return self._storage    

    # @property
    # def data(self):
    #     """
    #     Data used in request.
        
    #     :returns: dict
    #     """
    #     if not isinstance(self._data, dict):
    #         raise WrongDataType(self._data, dict)
    #     return self._data   

    # @property
    # def cookie(self):
    #     """
    #     Cookie used in request.
        
    #     :returns: dict
    #     """
    #     if not isinstance(self._cookie, dict):
    #         raise WrongDataType(self._cookie, dict)
    #     return self._cookie

    # @property
    # def url(self):
    #     """
    #     Url used in request.
        
    #     :returns: str
    #     """
    #     if not isinstance(self._url, str):
    #         raise WrongDataType(self._url, str)
    #     return self._url

    # @property
    # def response(self):
    #     """
    #     Response container from `aiohttp.ClientSession.response <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession.response>`_.
        
    #     :returns: :class:`~apollo.request.Response`
    #     """
    #     if not isinstance(self._response, Response):
    #         raise WrongDataType(self._response, Response)   
    #     return self._response

    # @response.setter
    # def response(self, value):
    #     self._response = value
    #     return value

    # @property
    # def storage_criteria(self):
    #     """
    #     Any function that will manipulate :class:`~apollo.request.Response` and return True or False.

    #     :returns: lambda
    #     """        
    #     return self._storage_criteria