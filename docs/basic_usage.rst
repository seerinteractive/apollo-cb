.. _basic_usage:

Basic Usage
===========

This section will cover making the minimum requests with 
:ref:`attributes` and :ref:`auth_usage` using 
:class:`~apollo.ApolloCB`.

Building Requests
-----------------

There are two key core attributes of a request:

.. toctree::
    :maxdepth: 3

    Authentication <auth_index>
    Request Attributes <request/attributes>

.. _basic_auth:

API Authentication
~~~~~~~~~~~~~~~~~~
Use the :class:`~apollo.auth.base.AuthBase` class to create custom API authentication.

:func:`~apollo.auth.base.AuthBase.param`, :func:`~apollo.auth.base.AuthBase.header` or :func:`~apollo.auth.base.AuthBase.auth`
can be used for authentication. Below we're implementing :func:`~apollo.auth.base.AuthBase.param`.

.. code-block:: python

    from apollo.auth.base import AuthBase

    class MyAPI(AuthBase):
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

    api_auth = MyAPI(
        api_key = '123'
    )

.. _basic_attributes:


Request Attributes
~~~~~~~~~~~~~~~~~~
Often times  we make more than one request when using an http request library. That means
we need to generate a list of urls and / or parameters and / or auth to make unique requests.
We can use a simple zipping technique to make these multiple requests but this creates a lot
of extra, unnecessary code. 

:class:`~apollo.ApolloCB` 
implements a wrapper to generate lists of urls, params, headers, data, 
cookies, etc. which are then zipped and requests made. 
These wrappers can be found in the :ref:`attributes` module.

The below example uses :func:`~apollo.request.attributes.Url` (which implements 
the `str format method <https://docs.python.org/2/library/functions.html#format>`_ 
to generate a list of urls) and :func:`~apollo.request.attributes.Param` attributes. 

URL::

    from apollo.request.attributes import Url

    URL_LIMIT = 20

    url = Url(
        path_format = "http://httpbin.org/anything/{a}/{b}",
        a = [f'folder{n}' for n in range(URL_LIMIT)],
        b = [f'subfolder{n}' for n in range(URL_LIMIT)]
    )

*yields*:: 

    http://httpbin.org/anything/folder0/subfolder0
    http://httpbin.org/anything/folder1/subfolder1
    ...
    http://httpbin.org/anything/folder18/subfolder18
    http://httpbin.org/anything/folder19/subfolder19

Param::

    from apollo.request.attributes import Param

    param = Param(
        static = {'param_a': 'a'},
        dynamic = {'b': [n for n in range(URL_LIMIT)]}
    )

*yields*::

    {'b': '0', 'param_a': 'a'}
    {'b': '1', 'param_a': 'a'}
    ...
    {'b': '18', 'param_a': 'a'}
    {'b': '19', 'param_a': 'a'}

Note: If uneven lists are given, the last value of the shorter list will be
repeated (see :func:`~apollo.utils.helpers.zip_longest_ffill`). To modify 
this functionality, use the zip_type argument.

.. _basic_rate_limiting:

Rate Limiting
~~~~~~~~~~~~~

:class:`~apollo.ApolloCB` runs asynchronously and can easily cause a 
`DDOS attack <https://en.wikipedia.org/wiki/Denial-of-service_attack>`_ for vulnerable
websites. To avoid this, the :class:`~apollo.utils.RateLimit` class protects endpoints and storage from
being overwhelmed. The below example shows the API rate limit will be 5 requests 
every 5 seconds and storage one request every second. The default RateLimit is a rate of 5
every 5 seconds.

.. code-block:: python

    from apollo.utils import RateLimit

    api_rate_limit = RateLimit(
        rate = 5,
        limit = 5
    )


Executing Requests
------------------

Once :ref:`attributes` and :ref:`auth_usage` are complete, it's time
to make the request using :class:`~apollo.ApolloCB`.


ApolloCB uses the above values to make requests::

    from apollo import ApolloCB

    rf = ApolloCB(
        method = "GET", 
        url = url,
        param = param,
        api_auth = api_auth,        
        verbose = True,
        save = True,
        api_rate_limit = api_rate_limit,
    )

    a = rf.execute()

*yields*::



[08:23:10] Url http://httpbin.org/anything/folder0/subfolder0?b=0&param_a=a&my_api_key=123, Status 200
[08:23:10] Url http://httpbin.org/anything/folder3/subfolder3?b=3&param_a=a&my_api_key=123, Status 200
[08:23:10] Url http://httpbin.org/anything/folder2/subfolder2?b=2&param_a=a&my_api_key=123, Status 200
[08:23:10] Url http://httpbin.org/anything/folder1/subfolder1?b=1&param_a=a&my_api_key=123, Status 200
[08:23:10] Url http://httpbin.org/anything/folder4/subfolder4?b=4&param_a=a&my_api_key=123, Status 200
[08:23:15] Url http://httpbin.org/anything/folder9/subfolder9?b=9&param_a=a&my_api_key=123, Status 200
[08:23:15] Url http://httpbin.org/anything/folder5/subfolder5?b=5&param_a=a&my_api_key=123, Status 200
[08:23:15] Url http://httpbin.org/anything/folder6/subfolder6?b=6&param_a=a&my_api_key=123, Status 200
[08:23:15] Url http://httpbin.org/anything/folder8/subfolder8?b=8&param_a=a&my_api_key=123, Status 200
[08:23:15] Url http://httpbin.org/anything/folder7/subfolder7?b=7&param_a=a&my_api_key=123, Status 200