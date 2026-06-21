from json import loads, JSONDecodeError
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
import uuid


def test_v1_account_token():
    
    # Регистрация пользователя
    account_api = AccountApi(host='http://185.185.143.231:5051')
    login_api = LoginApi(host='http://185.185.143.231:5051')
    mailhog_api = MailhogApi(host='http://185.185.143.231:5025')
    
    login = f'user_{uuid.uuid4().hex[:8]}'
    email = f'{login}@mail.ru'
    password = '12345678'
    
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    
    response = account_api.post_v1_account(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f'Пользователь не был создан, {response.json()}'
    
    # Получение письма в почтовом сервере
    response = mailhog_api.get_api_v2_messages()
    
    print(response.status_code)
    print(response.text)
    # pprint.pprint(response.json())
    assert response.status_code == 200, 'Письма не были получены'
    
    # Получение токена
    token = get_token_by_login(login, response)
    assert token is not None, f'Токен для пользователя {login} не был получен'
    
    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'Пользователь не был активирован'

"""
def get_token_by_login(
        login,
        response
        ):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(user_login)
            print(token)
            assert token is not None, 'Письмо с токеном о не пришло'
    return token
"""


def get_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()['items']:
        try:
            user_data = loads(item['Content']['Body'])
        except (JSONDecodeError, KeyError):
            continue  # ← ФИКС: пропускаем плохие письма
        
        user_login = user_data['Login']  # ← ОСТАЛОСЬ КАК БЫЛО
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(user_login)
            print(token)
            assert token is not None, 'Письмо с токеном о не пришло'
    return token