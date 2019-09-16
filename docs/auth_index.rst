.. _auth_usage:

Authentication
==============

A request can (but it's not necessary) accept authentication from 
either :ref:`prebuilt` or :class:`~apollo.auth.base.AuthBase`.

Example usage
--------------

Custom API
~~~~~~~~~~

Use the :class:`~apollo.auth.base.AuthBase` class.

.. code-block::

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

Prebuilt API
~~~~~~~~~~~~

Use :ref:`prebuilt`.

.. code-block::

  from apollo.auth import Pipedrive

  api_auth = Pipedrive(api_key = '123')


.. toctree::
  :maxdepth: 2
  :hidden:

  AuthBase <auth/base>
  APIs <auth/apis>
  




Indices and tables

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

