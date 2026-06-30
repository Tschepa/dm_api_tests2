import time
from retry import retry
from json import (
    loads,
    JSONDecodeError,
)

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
        
    def auth_client(self, login: str, password: str):
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data={'login':login, 'password':password}
        )
        token = {"x-dm-auth-token": response.headers["x-dm-auth-token"]}
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)
        
    def register_new_user(self, login:str, password: str, email:str):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f'Пользователь не был создан, {response.json()}'
        
        token = self.get_token_by_login(login=login)
        assert token is not None, f'Токен для пользователя {login} не был получен'
        
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, 'Пользователь не был активирован'
        
        return response
    
    def user_login(
            self,
            login:str,
            password:str,
            remember_me: bool = True
    ):
        json_data = {
            'login': login,
            'password': password,
            'remember_me': True,
        }
        
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, 'Пользователь не авторизован'
        return response
    
    def activate_user(
            self,
            token: str
            ):
        """
        Активация пользователя по токену
        """
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, 'Активация не удалась'
        return response
    
    def change_email(
            self,
            login:str,
            password: str,
            changed_email:str
    ):
        
        json_data = {
            'login': login,
            'password': password,
            'email': changed_email
        }
        
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, 'Имейл не изменен'
        
        # Авторизация с измененным имейлом
        
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }
        
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 403, 'Пользователь с измененным имейлом авторизован до активации нового токена'
        
        # Получение токена о смене имейла
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, 'Письмо об изменении имейла не было получено'
        
        token = self.get_token_by_login(login=login)
        assert token is not None, f'Токен об изменении имейла для пользователя {login} не был получен'
        
        # Активация пользователя с измененным имейлом
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, 'Пользователь с измененным имейлом не был активирован'
        
        # Авторизация пользователя с измененным имейлом
        self.user_login(login=login, password=password)
    
    def change_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str
            ):
        token = self.user_login(login=login, password=old_password)
        self.dm_account_api.account_api.post_v1_account_password(
            json={
                "login": login,
                "email": email
            },
            headers={
                "x-dm-auth-token": token.headers["x-dm-auth-token"]
            },
        )
        token = self.get_token(login=login, token_type="reset")
        self.dm_account_api.account_api.put_v1_account_password(
            json={
                "login": login,
                "oldPassword": old_password,
                "newPassword": new_password,
                "token": token
            }
        )
    
    @retrier
    def get_token_by_login(
            self,
            login
    ):
        token = None
        time.sleep(3)
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
        return token
    
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
            user_data = loads(item["Content"]["Body"])
            user_login = user_data["Login"]
            activation_token = user_data.get("ConfirmationLinkUrl")
            reset_token = user_data.get("ConfirmationLinkUri")
            if user_login == login and activation_token and token_type == "activation":
                token = activation_token.split("/")[-1]
            elif user_login == login and reset_token and token_type == "reset":
                token = reset_token.split("/")[-1]
        
        return token