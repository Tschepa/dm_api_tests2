import time
from json import (
    loads,
    JSONDecodeError,
)

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

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
            token: str,
            password: str,
            newPassword: str
    ):
        auth_token = self.dm_account_api.account_api.session.headers.get("x-dm-auth-token")
        json_data = {
            'login': login,
            'token': token,
            'password': password,
            'newPassword': newPassword

        }
        headers = {
            'X-Dm-Auth-Token': auth_token
        }
        response = self.dm_account_api.account_api.put_v1_account_password(json_data=json_data, headers=headers)
        assert response.status_code == 200, 'Пароль не изменен'
        return response
        
        """
        # Получение токена о смене пароля
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, 'Письмо об изменении пароля не было получено'
        
        token = self.get_token_by_login(login, response)
        assert token is not None, f'Токен об изменении пароля для пользователя {login} не был получен'
        return token
        # Активация токена
    
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, 'Пользователь с измененным имейлом не был активирован'
        """
    
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