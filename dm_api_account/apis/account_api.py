import requests

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):
    """def __init__(
            self,
            host,
            headers=None
        ):
        self.host = host
        self.headers = headers
        УДАЛЕНО,  так как наслодовали у RestClient, пкм добавили импорт
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
        response = self.post(path=f'/v1/account', json=registration.model_dump(exclude_none=True, by_alias=True))
        return response
    
    def put_v1_account_token(
        self,
        token,
        validate_response = True
    ):
        """
        Activate registered user
        :param token:
        :return:
        """
        response = self.put(
            path=f'/v1/account/{token}',
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response
    
    def put_v1_account_email(
        self,
        change_email: ChangeEmail,
    validate_response=True
    ):
        """
        Change registered user email
        :param json_data:
        :return:
        """
        response = self.put(
            path = f'/v1/account/email',
            json=change_email.model_dump(by_alias=True)
        )
        
        assert response.status_code == 200, 'Email не изменен'
        if validate_response:
            return UserEnvelope(**response.json())
        return response
    
    def get_v1_account(
        self,
        validate_response=True,
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
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response
    
    def put_v1_account_password(
        self,
        change_password: ChangePassword,
        validate_response=True
    ):
        """
        Change registered user email
        :param json_data:
        :return:
        """
        response = self.put(
            path=f'/v1/account/password',
            json=change_password.model_dump(by_alias=True)
        )
        
        assert response.status_code == 200, 'Password не изменен'
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    
    def post_v1_account_password(
        self,
        reset_password:ResetPassword,
        headers=None,
        validate_response = True
    ):
        response = self.post(
            path='/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True),
            headers=headers
        )
        assert response.status_code == 200, 'Запрос на смену пароля не отправлен'
        if validate_response:
            return UserEnvelope(**response.json())
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