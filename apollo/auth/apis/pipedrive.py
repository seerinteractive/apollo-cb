"""
This module connects users to the Pipedrive API
"""
#standard
import types

#third party
import attr
from attr.validators import instance_of


#local
from apollo.auth.base import AuthBase


@attr.s
class Pipedrive(AuthBase):
    """Read more about the Pipedrive API at `their docs <https://developers.pipedrive.com/docs/api/v1/>`_.

    :type api_key: str
    :param api_key: Find your `API key <https://support.pipedrive.com/hc/en-us/articles/207344545-How-can-I-find-my-personal-API-key->`_.

    :type user_agent: str
    :param user_agent: User agent used in the request.

    """

    api_key = attr.ib(converter = attr.converters.optional(str), repr=False, validator = instance_of(str))
    user_agent = attr.ib(default = "Apollo-CB", converter = attr.converters.optional(str))

    @property
    def base(self,):
        """The url endpoint used to make requests. The default is: `https://api.pipedrive.com/v1 <https://api.pipedrive.com/v1>`_

        """
        return "https://api.pipedrive.com/v1"

    @property
    def header(self):
        """The header tells Pipedrive to provide a JSON response.

        """
        return {
            "Accept": "application/json, */*",
            "content-type": "application/json",
            "User-Agent": self.user_agent,
        }

    @property
    def param(self,):
        """The ``api_key`` is passed into parameter for authentication.

        """
        return {
            "api_token": self.api_key
        }
