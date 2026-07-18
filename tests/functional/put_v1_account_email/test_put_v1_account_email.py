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

@allure.suite('Тесты на проверку метода PUT v1/account/email')
@allure.sub_suite('Позитивные тесты')
@allure.title('Проверка изменения эл. адреса пользователя')
def test_v1_account_email(account_helper, prepare_user):
    
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    
    # Регистрация пользователя
    account_helper.register_new_user(login=login, password=password, email=email)
    auth_token = account_helper.user_login(login=login, password=password)
    
    # Изменение имейла_403 авторизация_активация токена_авторизация
    changed_email = f'{login}@ya.ru'
    
    account_helper.change_email(login=login, password=password, changed_email=changed_email)