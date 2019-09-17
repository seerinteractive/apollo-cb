ApolloCB
========

Making API requests and storing responses usually requires a lot of boilerplate code. Authentication, intercepting responses before storage, 
issues with threading on different machines and many more challenges and frustrations -- resulting in thousands of lines of 
unnecessary code -- are common when building custom clients.

ApolloCB is a Python client that aims to simplify the calling APIs by handling authentication, rate limiting external API requests and storage, asynchronously. 

Getting Started
---------------


Mac/Linux
~~~~~~~~~

.. code-block:: bash

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install apollo-cb

Windows
~~~~~~~

.. code-block:: bash

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install apollo-cb


API Authentication
~~~~~~~~~~~~~~~~~~
Use the AuthBase class to create custom API authentication.

param, header or auth
can be used for authentication. Below we're implementing param.

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

ApolloCB 
implements a wrapper to generate lists of urls, params, headers, data, 
cookies, etc. which are then zipped and requests made. 
These wrappers can be found in the attributes module.

The below example uses Url (which implements 
the `str format method <https://docs.python.org/2/library/functions.html#format>`_ 
to generate a list of urls) and Param attributes. 

URL

.. code-block:: python

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

Param

.. code-block:: python

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
repeated (see zip_longest_ffill). To modify 
this functionality, use the zip_type argument.

.. _basic_rate_limiting:

Rate Limiting
~~~~~~~~~~~~~

ApolloCB runs asynchronously and can easily cause a 
`DDOS attack <https://en.wikipedia.org/wiki/Denial-of-service_attack>`_ for vulnerable
websites. To avoid this, the RateLimit class protects endpoints and storage from
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

Once attributes and authentication are complete, it's time
to make the request using ApolloCB.


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