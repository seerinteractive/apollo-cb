"""
This module connects users to the BambooHR API
"""

#third party
import attr

#local
from apollo.auth.base import AuthBase


@attr.s
class BambooHR(AuthBase):
    """Read the `BambooHR <https://documentation.bamboohr.com/docs>`_ API docs for information on how to obtain your API key.

    :type api_key: str
    :param api_key: Read how to obtain an API key `here <https://documentation.bamboohr.com/docs#section-authentication>`_.

    :type user_agent: str
    :param user_agent: User agent used in the request.

    """

    api_key = attr.ib(converter = str, repr = False)
    subdomain = attr.ib(converter = str)
    user_agent = attr.ib(default = "Apollo-CB", converter = attr.converters.optional(str))

    @property
    def base(self):
        """The url endpoint used to make requests. The default is: `https://api.bamboohr.com/api/gateway.php <https://api.bamboohr.com/api/gateway.php>`_
        """
        
        return f'https://api.bamboohr.com/api/gateway.php/{self.subdomain}/v1'

    @property
    def header(self):
        """The header tells BambooHR to provide a JSON response.

        """
        return {
            "Accept": "application/json", 
            "User-Agent": self.user_agent
        }

    @property
    def auth(self):
        """The ``api_key`` is the username and the password is blank.

        """
        return (self.api_key, "")
