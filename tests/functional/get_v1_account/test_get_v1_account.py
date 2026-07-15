from datetime import datetime

import requests
from hamcrest import (
    assert_that,
    all_of,
    has_property,
    has_properties,
    equal_to,
    starts_with,
    instance_of,
)

from assertpy import assert_that, soft_assertions

from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http
from dm_api_account.models.user_details_envelope import UserRole
from services.dm_api_account import DMApiAccount


def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
    GetV1Account.check_response_values_account(response)
    print(response)


def test_get_v1_account_no_auth(account_helper):
    account_helper.dm_account_api.account_api.session.headers.clear()
    account_helper.dm_account_api.login_api.session.headers.clear()
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)