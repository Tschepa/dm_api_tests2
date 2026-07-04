import requests

from dm_api_account.models.registration import Registration
from restclient.client import RestClient


class AccountApi(RestClient):
    """def __init__(
            self,
            host,
            headers=None
        ):
        self.host = host
        self.headers = headers
        УДАЛЕНО, так как наслодовали у RestClient, пкм добавили импорт
    """
    def post_v1_account(
            self,
            registration: Registration
            ):
        """
        Register new user

        :param json_data:
        :return:
        """
        """response = requests.post(
            url=f'{self.host}/v1/account',
            json=json_data
        ) """
        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response
    
    def put_v1_account_token(
            self,
            token
            ):
        """
        Activate registered user
        :param token:
        :return:
        """
        response = self.put(
            path=f'/v1/account/{token}',
        )
        assert response.status_code == 200, 'Пльзователь не активирован'
        return response
    
    def put_v1_account_email(
            self,
            json_data
            ):
        """
        Change registered user email
        :param json_data:
        :return:
        """
        response = self.put(
            path = f'/v1/account/email',
            json=json_data
        )
        
        assert response.status_code == 200, 'Email не изменен'
        return response
    
    def get_v1_account(
            self,
            **kwargs
    ):
        """
        Get current user

        :param json_data:
        :return:
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
        )
        return response
    
    def put_v1_account_password(
            self,
            json_data
    ):
        """
        Change registered user email
        :param json_data:
        :return:
        """
        response = self.put(
            path=f'/v1/account/password',
            json=json_data
        )
        assert response.status_code == 200, 'Password не изменен'
        return response
    
    def post_v1_account_password(
            self,
            json,
            headers=None
            ):
        response = self.post(
            path='/v1/account/password',
            json=json,
            headers=headers
        )
        assert response.status_code == 200, 'Запрос на смену пароля не отправлен'
        return response
    
    def delete_v1_account_login(
            self,
            **kwargs
    ):
        response = self.delete(
            path=f'/v1/account',
            **kwargs
        )
        return response
    
    def delete_v1_account_login_all(
            self,
            **kwargs
    ):

        response = self.delete(
            path=f'/v1/account',
            **kwargs
        )
        return response