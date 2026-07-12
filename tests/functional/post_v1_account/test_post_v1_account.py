from datetime import datetime

from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    instance_of,
    has_properties,
    equal_to,
)

from checkers.http_checkers import check_status_code_http

def test_v1_account(
        account_helper,
        prepare_user
        ):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    
    # Регистрация пользователя
    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    
    assert_that(
        response,
        all_of(
            has_property('resource', has_property('login', starts_with('user'))),
            has_property('resource', has_property('registration', instance_of(datetime))),
            has_property(
                'resource',
                has_properties(
                    {
                        'rating': has_properties(
                            {
                                'enabled': equal_to(True),
                                'quality': equal_to(0),
                                'quantity': equal_to(0)
                            }
                        )
                    }
                )
            )
        )
    )
    print(response)
    
def test_post_v1_account_short_password(account_helper, short_password_user):
    with check_status_code_http(400, "Validation failed", "Password", "Short"):
        account_helper.register_new_user(
            short_password_user.login,
            short_password_user.password,
            short_password_user.email
        )


def test_post_v1_account_invalid_email(account_helper, invalid_email_user):
    with check_status_code_http(400, "Validation failed", "Email", "Invalid"):
        account_helper.register_new_user(
            invalid_email_user.login,
            invalid_email_user.password,
            invalid_email_user.email
        )


def test_post_v1_account_short_login(account_helper, short_login_user):
    with check_status_code_http(400, "Validation failed", "Login", "Short"):
        account_helper.register_new_user(
            short_login_user.login,
            short_login_user.password,
            short_login_user.email
        )