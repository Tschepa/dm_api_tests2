from datetime import datetime
from operator import contains

from assertpy import soft_assertions
from hamcrest import (
    assert_that,
    starts_with,
    all_of,
    has_property,
    has_properties,
    equal_to,
    instance_of,
)

from checkers.http_checkers import check_status_code_http
from dm_api_account.models.user_details_envelope import UserRole


class GetV1Account:

    @classmethod
    def check_response_values_account(
                cls,
                response
        ):
            with check_status_code_http(200, ''):
                today = datetime.now().strftime('%Y-%m-%d')
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
            assert_that(str(response.resource.online), starts_with(today))
            print('Проверка даты прошла')
            assert_that(response.resource.roles), contains(UserRole.GUEST.value, UserRole.PLAYER.value)
            print('Проверка ролей прошла')
            
            '''
            with soft_assertions():
                assert_that(response.resource.login).starts_with('user')
                print('Проверка логина прошла')
                assert_that(response.resource.online).is_instance_of(datetime)
                print('Проверка даты прошла')
                assert_that(response.resource.roles).contains(UserRole.GUEST.value, UserRole.PLAYER.value)
                print('Проверка ролей прошла')'''