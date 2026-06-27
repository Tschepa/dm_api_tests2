import requests

from restclient.client import RestClient


class MailhogApi(RestClient):
    """ def __init__(
            self,
            host,
            headers=None
        ):
        self.host = host
        self.headers = headers
    """
    def get_api_v2_messages(
            self,
            limit = '50'
            ):
        params = {
            'limit': limit,
        }
    
        """
            Get users emails
        """
        response = self.get(
            path=f'/api/v2/messages',
            params=params,
            verify=False
        )
        return response