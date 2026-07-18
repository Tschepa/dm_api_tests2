import time

import allure
from retrying import retry
from json import (
    loads,
    JSONDecodeError,
)

from checkers.http_checkers import check_status_code_http
from clients.http.dm_api_account.models.change_email import ChangeEmail
from clients.http.dm_api_account.models.change_password import ChangePassword
from clients.http.dm_api_account.models.login_credentials import LoginCredentials
from clients.http.dm_api_account.models.registration import Registration
from clients.http.dm_api_account.models.reset_password import ResetPassword
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

def retry_if_result_none(result):
    """Возвращает True, если результат None (нужно повторить)"""
    return result is None

def retrier(
        function
):
    def wrapper(
            *args,
            **kwargs
    ):
        token = None
        count = 0
        while token is None:
            print(f'Попытка получения токена номер {count}')
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError('Превышено кол-во попыток получения акт-го токена')
            if token:
                return token
            time.sleep(1)
        return response
    return wrapper
    
class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog:MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog
    
    @allure.step('Авторизация пользователя')
    def auth_client(self, login: str, password: str):
        response = self.user_login(
            login=login,
            password=password
        )
        token = {"x-dm-auth-token": response.headers["x-dm-auth-token"]}
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)
    
    @allure.step('Регистрация нового пользователя')
    def register_new_user(self, login:str, password: str, email:str):
        registration = Registration(
            login=login,
            email=email,
            password=password
        )
        
        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f'Пользователь не был создан, {response.json()}'
        start_time = time.time()
        token = self.get_token(login=login, token_type="activation")
        end_time = time.time()
        assert end_time -  start_time < 3, 'Время ожидания активации превышено'
        assert token is not None, f'Токен для пользователя {login} не был получен'
        response = self.activate_user(token=token)
        return response
    
    @allure.step('Аутентификация пользователя')
    def user_login(
            self,
            login:str,
            password:str,
            remember_me: bool = True,
            validate_response=False,
            validate_headers = False
    ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me,
        )
        
        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response
        )
        if validate_headers:
            assert response.headers['x-dm-auth-token'], 'Токен для пользователя не был получен'
        return response
    
    @allure.step('Получение токена при активации')
    def activate_user(
            self,
            token: str
            ):
        """
        Активация пользователя по токену
        """
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response
    
    @allure.step('Изменение email')
    def change_email(
            self,
            login:str,
            password: str,
            changed_email:str,
            validate_response=True
    ):
        
        change_data = ChangeEmail(
            login=login,
            password=password,
            email=changed_email
        )
        
        response = self.dm_account_api.account_api.put_v1_account_email(change_email=change_data, validate_response=validate_response)
        
        # Авторизация с измененным имейлом
        
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=True
        )
        
        ''' response = self.dm_account_api.login_api.post_v1_account_login(login_credentials=login_credentials,
        validate_response=False)
        assert response.status_code == 403, 'Пользователь с измененным имейлом авторизован до активации нового токена'''''
        with check_status_code_http(403, 'User is inactive. Address the technical support for more details'):
            self.dm_account_api.login_api.post_v1_account_login(
                login_credentials=login_credentials,
                validate_response=False)
            
            # Получение токена о смене имейла
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, 'Письмо об изменении имейла не было получено'
        
        token = self.get_token(login=login, token_type="activation")
        assert token is not None, f'Токен об изменении имейла для пользователя {login} не был получен'
        
        # Активация пользователя с измененным имейлом
        response = self.dm_account_api.account_api.put_v1_account_token(token=token, validate_response=False)
        assert response.status_code == 200, 'Пользователь с измененным имейлом не был активирован'
        
        # Авторизация пользователя с измененным имейлом
        self.user_login(login=login, password=password)
    
    @allure.step('Изменение пароля')
    def change_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str,
            validate_response = True
        ):
        token = self.user_login(login=login, password=old_password)
        self.dm_account_api.account_api.post_v1_account_password(
            reset_password=ResetPassword(login=login, email=email),
            headers={
                "x-dm-auth-token": token.headers["x-dm-auth-token"]
            },
            validate_response = validate_response
        )
        token = self.get_token(login=login, token_type="reset")
        change_data = ChangePassword(
            login=login,
            token=token,
            oldPassword=old_password,
            newPassword=new_password
        )
        response = self.dm_account_api.account_api.put_v1_account_password(
            change_password=change_data,
            validate_response=validate_response
        )
        return response
    
    @allure.step('Логаут пользователя на всех устройствах')
    def logout_all(
            self,
            headers = None
    ):
        """Выход из системы на всех устройствах"""
        
        response = self.dm_account_api.login_api.delete_v1_account_login_all(headers=headers)
        assert response.status_code == 204, 'Выход на всех устройствах не выполнен'
        return response
    
    """@retrier
    def get_token_by_login(
            self,
            login
    ):
        token = None
        time.sleep(1)
        response = self.mailhog.mailhog_api.get_api_v2_messages()

        for item in response.json()['items']:
            try:
                user_data = loads(item['Content']['Body'])
            except (JSONDecodeError, KeyError):
                continue  # ← ФИКС: пропускаем плохие письма
            
            user_login = user_data['Login']  # ← ОСТАЛОСЬ КАК БЫЛО
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                print(user_login)
                print(token)
                assert token is not None, 'Письмо с токеном о не пришло'
        return token"""

    
    @retry(
        stop_max_attempt_number=5,
        retry_on_result=retry_if_result_none,
        wait_fixed=1000
    )
    def get_token(
            self,
            login,
            token_type="activation"
    ):
        """
        Получение токена активации или сброса пароля
        Args:
            login: логин пользователя
            token_type: тип токена (activation или reset)
        Returns:
            токен активации или сброса пароля
        """
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()["items"]:
            try:
                user_data = loads(item["Content"]["Body"])
            except (JSONDecodeError, KeyError):
                continue
                
            user_login = user_data["Login"]
            activation_token = user_data.get("ConfirmationLinkUrl")
            reset_token = user_data.get("ConfirmationLinkUri")
            if user_login == login and activation_token and token_type == "activation":
                token = activation_token.split("/")[-1]
            elif user_login == login and reset_token and token_type == "reset":
                token = reset_token.split("/")[-1]
        
        return token