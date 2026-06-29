from json import loads

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog:MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog
        
    def register_new_user(self, login:str, password: str, email:str):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f'Пользователь не был создан, {response.json()}'
        
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, 'Письма не были получены'
        
        token = self.get_token_by_login(login=login, response=response)
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
        """ ПЕРЕНЕСЕНО В ТЕСТ
        # Авторизация с измененным имейлом
        
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }
        
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 403, 'Пользователь с измененным имейлом авторизован до активации нового токена'
        """
        # Получение токена о смене имейла
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, 'Письмо об изменении имейла не было получено'
        
        token = self.get_token_by_login(login, response)
        assert token is not None, f'Токен об изменении имейла для пользователя {login} не был получен'
        return token

        """ ПЕРЕНЕСЕНО В ТЕСТ
        
        # Активация пользователя с измененным имейлом
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, 'Пользователь с измененным имейлом не был активирован'
        """
        """ ПЕРЕНЕСЕНО В ТЕСТ
        
        # Авторизация пользователя с измененным имейлом
        self.user_login(login=login, password=password)"""
        
    @staticmethod
    def get_token_by_login(
            login,
            response
    ):
        token = None
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