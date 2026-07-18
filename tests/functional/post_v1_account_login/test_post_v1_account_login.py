import allure

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
@allure.suite('Тесты на проверку метода POST v1/account/login')
@allure.sub_suite('Позитивные тесты')
@allure.title('Проверка аутентификации пользователя после регистрации')
def test_v1_account_login(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    
    # Регистрация пользователя
    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)