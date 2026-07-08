import requests

from dm_api_account.models.login_credentials import LoginCredentials
from restclient.client import RestClient


class LoginApi(RestClient):
    """def __init__(
            self,
            host,
            headers=None
        ):
        self.host = host
        self.headers = headers
    """
    def post_v1_account_login(
            self,
            login_credentials=LoginCredentials
            ):
        """
        Authenticate via credentials
        :param json_data:
        :param response:
        :return:
        """
        
        response = self.post(
            path=f'/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        return response
    
    def delete_v1_account_login(
            self,
            headers = None
    ):
        response = self.delete(
            path='/v1/account/login',
            headers = headers
        )
        return response
    
    def delete_v1_account_login_all(
            self,
            headers = None
    ):
        response = self.delete(
            path='/v1/account/login/all',
            headers = headers
        )
        
        return response