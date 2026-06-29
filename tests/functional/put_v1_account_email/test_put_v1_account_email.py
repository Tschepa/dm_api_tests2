from json import loads, JSONDecodeError
import uuid
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from helpers.account_helper import AccountHelper

from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration

from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount

import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)
def test_v1_account_email():
    
    mailhog_configuration = MailhogConfiguration(host='http://185.185.143.231:5025', disable_log=False)
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051', disable_log=False)
    
    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)
    
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)
    
    login = f'user_{uuid.uuid4().hex[:8]}'
    email = f'{login}@mail.ru'
    password = '12345678'
    
    # Регистрация пользователя
    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    
    # Изменение имейла (с возвращением токена в хелпере)
    changed_email = f'{login}@ya.ru'
    
    token = account_helper.change_email(login=login, password=password, changed_email=changed_email)
    
    # 403  при логине
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }
    response = account_helper.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 403, 'Доступ запрещён до активации'
    
    # активация токена
    response = account_helper.dm_account_api.account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, 'Пользователь с измененным имейлом не был активирован'
    
    # авторизация юзера с новым имейлом
    account_helper.user_login(login=login, password=password)