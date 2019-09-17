
#standard
from pprint import pprint as p
from collections import UserList
import types

#third party
import attr
from attr.validators import instance_of
from attr.validators import in_

#local
from apollo.builder.converters import DictConverter
from apollo.builder.converters import ListConverter

from apollo.builder.exceptions import MethodError
from apollo.builder.exceptions import WrongDataType

from apollo.request.api_request import APIRequest

from apollo.request.attributes import Param
from apollo.request.attributes import Param
from apollo.request.attributes import Header
from apollo.request.attributes import Auth
from apollo.request.attributes import Data
from apollo.request.attributes import Url
from apollo.request.attributes import Cookie

from apollo.storage.base import StorageBase

from apollo.utils import FilePattern
from apollo.utils.helpers import HttpAcceptedTypes
from apollo.utils.helpers import zip_longest_ffill

@attr.s
class RequestFactory(UserList):

    url = attr.ib(validator = instance_of(Url))
    method = attr.ib(default = 'GET', validator = in_(HttpAcceptedTypes.ACCEPTED_METHODS))
    param = attr.ib(default = Param(), validator = instance_of(Param))
    header = attr.ib(default = Header(), validator = instance_of(Header))
    auth = attr.ib(default = Auth(), validator = instance_of(Auth))
    req_data = attr.ib(default = Data(), validator = instance_of(Data))
    cookie = attr.ib(default = Cookie(), validator = instance_of(Cookie))
    zip_type = attr.ib(default = zip_longest_ffill, validator = instance_of(types.FunctionType))
    file_pattern = attr.ib(default = FilePattern(), validator = instance_of(FilePattern))
    mod_response = attr.ib(default = lambda x: x, validator = instance_of(types.FunctionType))
    storage = attr.ib(default = None, validator = instance_of((StorageBase, type(None))))
    verbose = attr.ib(default = False, validator = instance_of(bool))

    @property
    def data(self):

        zipped_request = self.zip_type(
            self.url, self.param, self.header, self.auth, self.req_data, self.cookie
        )

        requests = []

        for url, param, header, auth, data, cookie in zipped_request:
            r = APIRequest(
                method=self.method,
                url=url,
                param=param,
                header=header,
                auth=auth if any(auth) else None, #None if there isn't auth
                data=data,
                cookie=cookie,
                file_pattern=self.file_pattern,
                mod_response=self.mod_response,
                storage=self.storage,
                verbose=self.verbose,
            )
            requests.append(r)
        return requests