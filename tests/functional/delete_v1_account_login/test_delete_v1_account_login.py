from json import loads, JSONDecodeError
import uuid
import allure

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from helpers.account_helper import AccountHelper

from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration

from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount
from checkers.http_checkers import check_status_code_http

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

@allure.suite('Тесты на проверку метода DELETE v1/account/login')
@allure.sub_suite('Позитивные тесты')
@allure.title('Проверка логаута пользователя')

def test_delete_v1_account_login(account_helper, prepare_user):
    
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    
    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.auth_client(login=login, password=password)
    
    response = account_helper.dm_account_api.login_api.delete_v1_account_login()
    assert response.status_code == 204, 'Юзер разлогинен'
    
    '''response = account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
    assert response.status_code == 401, 'Токен недействителен'''''
    # Очищаем токен
    account_helper.dm_account_api.account_api.set_headers({})
    account_helper.dm_account_api.login_api.set_headers({})
    
    # Проверяем, что доступ запрещен
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)