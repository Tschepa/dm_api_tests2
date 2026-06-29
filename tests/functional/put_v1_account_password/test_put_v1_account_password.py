from json import loads, \
    JSONDecodeError
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


def test_v1_account_password(account_helper, prepare_user):
    mailhog_configuration = MailhogConfiguration(host='http://185.185.143.231:5025', disable_log=False)
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051', disable_log=False)
    
    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)
    
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)
    
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    newPassword = '87654321'
    
    # Регистрация пользователя
    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    
    # Забираем токен из авторизации
    response = account_helper.mailhog.mailhog_api.get_api_v2_messages()
    token = account_helper.get_token_by_login(login=login)
    
    account_helper.change_password(login=login, token=token, password=password, newPassword = newPassword)
    
    # Авторизация юзера с новым имейлом
    account_helper.user_login(login=login, password=password)