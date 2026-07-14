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

from checkers.http_checkers import check_status_code_http
from services.dm_api_account import DMApiAccount


def test_get_v1_account_auth(
        auth_account_helper
        ):
    with check_status_code_http(200, ''):
        response = auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
    assert_that(
        response,
        all_of(
            has_property('resource', has_property('login', starts_with('user'))),
            has_property('resource', has_property('online', instance_of(datetime))),
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
                        ),
                        'roles': equal_to(['Guest', 'Player']),
                        'settings': has_properties(
                            {
                                'color_schema': equal_to('Modern'),
                                'paging': has_properties(
                                    {
                                        'posts_per_page': equal_to(10),
                                        'comments_per_page': equal_to(10),
                                        'topics_per_page': equal_to(10),
                                        'messages_per_page': equal_to(10),
                                        'entities_per_page': equal_to(10)
                                    }
                                )
                            }
                        )
                    }
                )
            )
        )
    )
    print(response)
    

def test_get_v1_account_no_auth(account_helper):
    account_helper.dm_account_api.account_api.session.headers.clear()
    account_helper.dm_account_api.login_api.session.headers.clear()
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)