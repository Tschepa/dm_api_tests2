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

@allure.suite('Тесты на проверку метода PUT v1/account/password')
@allure.sub_suite('Позитивные тесты')
@allure.title('Проверка изменения пароля пользователя')
def test_v1_account_password(account_helper, prepare_user):
    
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    new_password = '87654321'
    
    # Регистрация пользователя
    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    
    account_helper.change_password(login=login, email=email, old_password=password, new_password = new_password)
    
    # Авторизация юзера с новым паролем
    account_helper.user_login(login=login, password=new_password)