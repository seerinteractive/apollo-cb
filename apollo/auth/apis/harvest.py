"""
This module connects users to the Harvest API
"""

#third party
import attr

#local
from apollo.auth.base import AuthBase


@attr.s
class Harvest(AuthBase):
    """Read more about the Harvest API at their `docs <https://help.getharvest.com/api-v2/>`_.

    :type access_token: str
    :param access_token: Learn more about the access token at `Harvest's authentication API documentation <https://help.getharvest.com/api-v2/authentication-api/authentication/authentication/>`_.

    :type account_id: str
    :param account_id: Learn more about the access token at `Harvest's authentication API documentation <https://help.getharvest.com/api-v2/authentication-api/authentication/authentication/>`_.

    :type user_agent: str
    :param user_agent: User agent used in the request.

    """

    access_token = attr.ib(converter = str, repr=False)
    account_id = attr.ib(converter = str)
    user_agent = attr.ib(default = "Apollo-CB", converter = str)

    @property
    def base(self):
        """The url endpoint used to make requests. The default is: `https://api.harvestapp.com/v2 <https://api.harvestapp.com/v2>`_

        """
        return "https://api.harvestapp.com/v2"

    @property
    def header(self):
        """The header is used to authenticate. The ``access_token`` is used as an Authorization Bearer and ``account_id`` is the ``Harvest-Account-Id``
        
        """
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Harvest-Account-Id": self.account_id,
            "User-Agent": self.user_agent,
        }
