#standard
from collections import UserList

#third party

import attr

#local

from apollo.builder.converters import ListConverter
from apollo.builder.converters import DictConverter

from apollo.utils.helpers import zip_longest_ffill




class Param(DictConverter):
    """Builds Url parameters

    :type static: dict
    :param static: Parameter that will persist in all :class:`apollo.request.attributes.Url` objects

    :type static: {'param': list}
    :param dynamic: Dynamic parameter

    :returns: List of dicts

    Example Usage:

    .. code-block:: 

        Param(
            static = {'param_a': 'a'},
            dynamic = {'b': [1, 2]}
        )
        >>> [{'param_a': a, 'b': 1}, {'param_a': a, 'b': 2}]

    """

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(static={self.static}, dynamic={self.dynamic})"
        )

class Url(UserList):
    """Builds Urls

    :type path_format: str
    :param path_format: String with possible formatting options

    :type path_args: list, str, int
    :param path_args: Arguments that correspond with the items in the path format.

    :returns: List of Urls

    Example Usage:

    .. code-block:: 

        Url(
            path_format = "http://httpbin.org/{a}/{b}/{c}", 
            a='a', b=['last','path'], c = ['it', 'is']
        )
        >>> ['http://httpbin.org/a/last/it', 'http://httpbin.org/a/path/is']

    """
    
    #attr cannot do kwargs

    def __init__(self, path_format, **path_args):
        self._path_format = path_format
        self._path_args = path_args

    def __repr__(self):
        return f"{self.__class__.__name__}(path_format={self.path_format}, dynamic={self.path_args})"

    @property
    def path_format(self,):
        return self._path_format

    @property
    def path_args(self,):
        return self._path_args

    @property
    def data(self,):

        conv_to_list = lambda x: [y if isinstance(y, list) else [y] for y in x]

        if self.path_args:

            zip_list = conv_to_list(self.path_args.values())
            a = zip_longest_ffill(*zip_list)
            vals = []
            for b in a:
                c = zip(self.path_args.keys(), b)
                vals.append(self.path_format.format(**dict(c)))
            return vals

        else:
            return [self.path_format]



class Cookie(DictConverter):
    """Builds list of cookies

    :type static: dict
    :param static: Cookie that will persist in all :class:`apollo.request.attributes.Url` objects

    :type static: {'param': list}
    :param dynamic: Dynamic cookie

    :returns: List of dicts

    Example Usage:

    .. code-block:: 

        Cookie(
            static = {'cookie': 'a'},
            dynamic = {'b': [1, 2]}
        )
        >>> [{'cookie': a, 'b': 1}, {'cookie': a, 'b': 2}]

    """

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(static={self.static}, dynamic={self.dynamic})"
        )


class Header(DictConverter):
    """Builds list of headers

    :type static: dict
    :param static: Header that will persist in all :class:`apollo.request.attributes.Url` objects

    :type static: {'param': list}
    :param dynamic: Dynamic header

    :returns: List of dicts

    Example Usage:

    .. code-block:: 

        Header(
            static = {'header': 'a'},
            dynamic = {'b': [1, 2]}
        )
        >>> [{'header': a, 'b': 1}, {'header': a, 'b': 2}]

    """

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(static={self.static}, dynamic={self.dynamic})"
        )

@attr.s
class Auth(UserList):
    """Builds auth for Urls

    :type username: str, int, list
    :param username: If a list, will return multiple tuples, if str, one tuple will be returned

    :type password: list, str, int
    :param password: If a list, will return multiple tuples, if str, one tuple will be returned

    :rtype: list(tuple(),tuple(),)
    :returns: List of of tuples

    Example Usage:

    .. code-block:: 

        Auth(
            username=[1,2], 
            password=[1,2]
        )
        >>> [(1, 1), (2, 2)]

    .. note::

        `zip <https://docs.python.org/3.3/library/functions.html#zip>`_ is used, so if one list is shorter than the other, it'll zip to the shortest.

    """

    username = attr.ib(default = '', converter = str)
    password = attr.ib(default = '', converter = str, repr = False)


    @property
    def data(self,):
        if isinstance(self.username, list) and isinstance(self.password, list):
            return [(un, pw) for un, pw in zip(self.username, self.password)]
        elif isinstance(self.username, (str, int)) and isinstance(
            self.password, (str, int)
        ):
            return [(self.username, self.password)]
        else:
            return [tuple()]


class Data(DictConverter):
    """Builds list of data

    :type static: dict
    :param static: Data that will persist in all :class:`apollo.request.attributes.Url` objects

    :type static: {'param': list}
    :param dynamic: Dynamic data

    :returns: List of dicts

    Example Usage:

    .. code-block:: 

        Data(
            static = {'data': 'a'},
            dynamic = {'b': [1, 2]}
        )
        >>> [{'data': a, 'b': 1}, {'data': a, 'b': 2}]

    """

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(static={self.static}, dynamic={self.dynamic})"
        )