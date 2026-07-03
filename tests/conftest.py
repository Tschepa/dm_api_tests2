from collections import namedtuple
from datetime import datetime
from json import loads, JSONDecodeError
import uuid
from collections import namedtuple
from datetime import datetime
from json import loads, JSONDecodeError
import uuid

import pytest

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
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
@pytest.fixture(scope='session')
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://185.185.143.231:5025', disable_log=False)
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client

@pytest.fixture(scope='session')
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account

@pytest.fixture(scope='session')
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper

@pytest.fixture
def auth_account_helper(mailhog_api, prepare_user):
    dm_api_configuration = DmApiConfiguration(
        host='http://185.185.143.231:5051',
        disable_log=False
    )
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    '''account_helper.auth_client(
        login='tsche911',
        password='12345678'
    )'''
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    
    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.auth_client(login=login, password=password)
    return account_helper

@pytest.fixture
def prepare_user():
    now = datetime.now()
    date = now.strftime('%d_%m_%Y_%H_%M_%S')
    login = f'user_{date}'
    email = f'{login}@mail.ru'
    password = '12345678'
    User = namedtuple('User', ['login', 'password', 'email'])
    user = User(login=login, password=password, email=email)
    return user