import os
from collections import namedtuple
from datetime import datetime
from json import loads, JSONDecodeError
import uuid
from collections import namedtuple
from datetime import datetime
from json import loads, JSONDecodeError
import uuid

import pytest
from swagger_coverage_py.reporter import CoverageReporter
from vyper import v
from pathlib import Path

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

options = (
    'service.dm_api_account',
    'service.mailhog',
    'user.login',
    'user.password',
)

@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    # Создаем папку принудительно
    os.makedirs("swagger-coverage-output/185.185.143.231_5051", exist_ok=True)
    reporter = CoverageReporter(api_name="dm-api-account", host="http://185.185.143.231:5051")
    reporter.setup("/swagger/Account/swagger.json")
    
    yield
    reporter.generate_report()
    reporter.cleanup_input_files()
'''@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    try:
        os.makedirs("swagger-coverage-output/185.185.143.231_5051", exist_ok=True)
        reporter = CoverageReporter(api_name="dm-api-account", host="http://185.185.143.231:5051")
        reporter.setup("/swagger/Account/swagger.json")
        yield
        reporter.generate_report()
        reporter.cleanup_input_files()
    except Exception as e:
        print(f"⚠️ Swagger coverage error: {e}")
        yield  # Тесты продолжаются'''

@pytest.fixture(scope='session', autouse=True)
def set_config(request):
    config = Path(__file__).joinpath('../../').joinpath('config')
    config_name = request.config.getoption('--env')
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f'{option}', request.config.getoption(f'--{option}'))
    yield

def  pytest_addoption(parser):
    parser.addoption('--env', action='store', default='stg', help='run stg')
    for option in options:
        parser.addoption(f'--{option}', action='store', default=None)

@pytest.fixture(scope='session')
def mailhog_api():
    #mailhog_configuration = MailhogConfiguration(host='http://185.185.143.231:5025', disable_log=False)
    mailhog_configuration = MailhogConfiguration(host=v.get('service.mailhog'), disable_log=False)
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client

@pytest.fixture(scope='session')
def account_api():
    #dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051', disable_log=False)
    dm_api_configuration = DmApiConfiguration(host=v.get('service.dm_api_account'), disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    return account

@pytest.fixture(scope='session')
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper

@pytest.fixture
def auth_account_helper(mailhog_api, prepare_user):
    '''dm_api_configuration = DmApiConfiguration(
        host='http://185.185.143.231:5051',
        disable_log=False
    )'''
    dm_api_configuration = DmApiConfiguration(
        host=v.get('service.dm_api_account'), disable_log=False
    )
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    '''account_helper.auth_client(
        login=v.get('user.login'),
        password=v.get('user.password')
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
    timestamp = now.strftime("%d_%m_%Y_%H_%M_%S_%f")
    login = f"user_{timestamp}"
    password = '12345678'
    email = f"{login}@mail.ru"
    User = namedtuple('User', ['login', 'password', 'email'])
    user = User(login=login, password=password, email=email)
    return user
    
@pytest.fixture
def short_password_user():

    """короткий пароль (менее 6 символов)"""
    
    User = namedtuple('User', ['login', 'password', 'email'])
    return User(
        login="test_short_pass",
        password="12345",
        email="test_short_pass@mail.ru"
    )

@pytest.fixture
def invalid_email_user():

    """невалидный email (без @)"""
    
    User = namedtuple('User', ['login', 'password', 'email'])
    return User(
        login="test_invalid_email",
        password="12345678",
        email="test_invalid_emailmail.ru"
    )

@pytest.fixture
def short_login_user():

    """короткий логин (1 символ)"""
    
    User = namedtuple('User', ['login', 'password', 'email'])
    return User(
        login="t",
        password="12345678",
        email="test_short_login@mail.ru"
    )