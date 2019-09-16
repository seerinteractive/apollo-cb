from apollo.request.abstract import RequestABC


class AuthBase(RequestABC):
    """The AuthBase is used to create custom API authentication. It's recommended to inherit the AuthBase in your custom class.

    You do not need to implement / override the :func:`~apollo.auth.base.AuthBase.param`, :func:`~apollo.auth.base.AuthBase.header` and :func:`~apollo.auth.base.AuthBase.auth` methods -- only those that are use for API authentication. 

    Example Usage:

    .. code-block::

        from apollo.auth.base import AuthBase

        class MyAPI(AuthBase):
        \"""My custom API\"""

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

    """

    def __rshift__(self, val):

        val.param.update(self.param)
        val.header.update(self.header)
        if self.auth:
            val.auth = self.auth
        return val

    @property
    def header(self):
        """If header authentication is necessary.

        :rtype: dict

        """
        return dict()

    @property
    def param(self):
        """If param authentication is necessary.

        :rtype: dict

        """
        return dict()

    @property
    def auth(self):
        """If auth authentication is necessary.

        :rtype: tuple

        """
        return tuple()
