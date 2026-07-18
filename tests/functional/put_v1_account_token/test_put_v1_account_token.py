import allure

import uuid

from helpers.account_helper import AccountHelper
from packages.restclient.configuration import Configuration as MailhogConfiguration
from packages.restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

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

@allure.suite('Тесты на проверку метода PUT v1/account/token')
@allure.sub_suite('Позитивные тесты')
@allure.title('Проверка активации зарегистрированного пользователя')
def test_v1_account_token():
    
    # Регистрация пользователя
    mailhog_configuration = MailhogConfiguration(host='http://185.185.143.231:5025', disable_log=False)
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051', disable_log=False)
    
    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)
    
    login = f'user_{uuid.uuid4().hex[:8]}'
    email = f'{login}@mail.ru'
    password = '12345678'
    
    account_helper.register_new_user(login=login, password=password, email=email)