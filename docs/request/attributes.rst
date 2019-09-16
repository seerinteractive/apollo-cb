.. _attributes:

Request Attributes
==================

Request attributes are passed into :class:`~apollo.ApolloCB` to create :class: `apollo.request.APIRequest`.
Keep in mind each of the below attributes create lists of strs, dicts or tuples.

There are six key components of a request:

* :class:`~apollo.request.attributes.Auth`
* :class:`~apollo.request.attributes.Cookie`
* :class:`~apollo.request.attributes.Data`
* :class:`~apollo.request.attributes.Header`
* :class:`~apollo.request.attributes.Param`
* :class:`~apollo.request.attributes.Url`

.. _attr_auth:

Auth
----

Authentication with a given API. This enables you to make different
authentication connections with a given API. Let's say you wanted to
use an API as 10 different users. You can use Auth to generate the 
authentication for those 10 users, which will be implemented by :class:`~apollo.ApolloCB`. 
Auth here will be added to any authentication used in :class:`~apollo.auth.base.AuthBase`.

.. _attr_cookie:

Cookie
------

A list of different cookies can be passed into the request -- helpful if 
sessions are used in the request.

.. _attr_data:

Data
----

Posting data to an API is quite common. Use :class:`~apollo.request.attributes.Data` 
to create a list of dicts that will be used in the request.

.. _attr_header:

Header
------

Authentication or other pieces of data can be passed via headers.
Use :class:`~apollo.request.attributes.Header` to create a list of headers. 
Headers here will be added to any authentication used in :class:`~apollo.auth.base.AuthBase`.

.. _attr_param:

Param
-----

Many APIs use url parameters with the GET REST method to access API data. 
Any parameters in Param will be added to any :func:`~apollo.auth.base.AuthBase.param` authentication 
in :class:`~apollo.auth.base.AuthBase`.

.. _attr_url:

Url
---

Many APIs use folders to access data. Use :class:`~apollo.request.attributes.Url` if 
you're generating folders. Note that any url will override the :class:`~apollo.auth.base.AuthBase`
url. Make sure you include the API base url in your request if using Url.

---------------------------------------------

.. automodule:: apollo.request.attributes
    :members:
    :show-inheritance: