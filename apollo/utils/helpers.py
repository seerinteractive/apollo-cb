#standard
from collections import namedtuple
from collections import UserString

#third party
import attr
from attr.validators import instance_of
from attr.validators import in_

#local
from apollo.builder.exceptions import WrongDataType


@attr.s
class RateLimit:
    """Sets the storage and API rate limits for :class:`~apollo.ApolloCB`.

    :type rate: int
    :param rate: The speed with which :class:`~apollo.ApolloCB` executes requests (in seconds).

    :type limit: int
    :param limit: The number of requests to be executed at one time.

    """
    rate = attr.ib(default = 5, converter = int)
    limit = attr.ib(default = 5, converter = int)

    @rate.validator
    def _(self, attribute, value):
        if value <= 0:
            raise ValueError(f"The rate must be over 0. You provided {self.rate}")

    @limit.validator
    def _(self, attribute, value):
        if value <= 0:
            raise ValueError(f"The limit must be over 0. You provided {self.limit}")

@attr.s
class FilePath(UserString):
    """FilePath is the str of the file path

    :type path: str
    :param path: The str of the file path

    :returns: str

    """
    
    path = attr.ib(converter = str)

    @property
    def data(self,):
        return self.path


class FilePattern:
    """The file pattern for saved objects, implemented by :class:`~apollo.ApolloCB`.

    :type lookup_obj: object
    :param lookup_obj: Object to lookup. Leave blank if self, is the first argument in file_func.

    :type file_func: lambda
    :param file_func: Function to create the file path.

    :type pattern_params: kwargs
    :param pattern_params: Kwargs used in the file_func.

    Example usage:

    .. code-block:: python

        from apollo.utils import FilePattern

        def file_func(self, custom_param):
        
            json = self.response.json
            
            request_method = json['method']
            b_param = json['args']['b']

            return f"{request_method}/{b_param}/{custom_param}"

        file_pattern = FilePattern(
            file_func = file_func,
            custom_param = 'there'
        )        

    :returns: :class:`~apollo.utils.FilePath`

    """

    def __init__(self, lookup_obj=None, file_func=None, **pattern_params):
        self._lookup_obj = lookup_obj
        self._file_func = file_func
        self._pattern_params = pattern_params

    @property
    def file_func(self,):
        """Function to create the file path.

        """
        return self._file_func

    @property
    def pattern_params(self,):
        return self._pattern_params

    @property
    def lookup_obj(self,):
        """Object to lookup. Leave blank if self, is the first argument in file_func.

        """
        return self._lookup_obj

    @lookup_obj.setter
    def lookup_obj(self, val):
        self._lookup_obj = val
        return val

    @property
    def path(self):
        """Implementation of the file_func, and pattern_params.

        :returns: :class:`~apollo.utils.FilePath`
        """

        if self.file_func:
            path = self.file_func(self.lookup_obj, **self.pattern_params)
            return FilePath(path=path)
        return FilePath(path="")


def zip_longest_ffill(*args):
    """Zip-like functionality, except it repeats the last value of the shorter list to the length of the longest list

    :type args: list of lists
    :param args: list(list, list, list)

    Example usage:

    .. code-block:: python

        zip_longest_ffill(*[[1,2],[1,2,3]])
        >>>[(1, 1), (2, 2), (2, 3)]

    """
    lists = [x if isinstance(x, list) else list(x) for x in args]
    max_total_len = max([len(l) for l in lists])

    ffill_lists = []

    for sub_list in lists:
        max_list_len = len(sub_list)
        max_diff = max_total_len - max_list_len

        # empty lists with no -1 index
        try:
            last_val = sub_list[-1]
            complete_list = sub_list + [last_val] * max_diff
        except:
            complete_list = [[] for _ in range(max_diff)]
        ffill_lists.append(complete_list)

    return zip(*ffill_lists)

class HttpAcceptedTypes:

    ACCEPTED_METHODS = ['GET', 'POST', 'PUT', 'DELETE']
    ACCEPTED_CONTENT_TYPES = {
        'json' : 'application/json',
        'xml': 'application/xml'
    }