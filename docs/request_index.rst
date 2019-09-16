.. _request_usage:

API Request & Response
======================

There are two elements of API calls: requests and responses.
Both can be called directly but are intended to be implemented by
:class:`~apollo.ApolloCB`.

Request
-------

:class:`~apollo.requestAPIRequest` uses the asyncio and aiohttp 
libraries to make and store API requests.

See: :class:`apollo.request.APIRequest`

Response
--------

aiohttp.Response is non-blocking and therefore cannot save information
like the Requests library. :class:`~apollo.request.Response` serves as a 
container for aiohttp.Response.

See: :class:`apollo.request.Response`

.. toctree::
  :maxdepth: 2
  
  Request <request/api>  

Indices and tables

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

