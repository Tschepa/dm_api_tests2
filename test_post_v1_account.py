import requests
import pprint
from json import loads
from account_api import AccountApi
from login_api import LoginApi
from mailhog_api import MailhogApi

def test_v1_account():
    # Регистрация пользователя
    account_api = AccountApi(host='http://185.185.143.231:5051')
    login_api = LoginApi(host='http://185.185.143.231:5051')
    mailhog_api = MailhogApi(host='http://185.185.143.231:5025')
    login = 'wow10'
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

    
    # Авторизация пользователя

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    
    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'Пользователь не авторизован'
    
    """пробую сама"""
    
    # Изменение имейла
    
    changed_email = f'{login}@ya.ru'
    json_data = {
        'login': login,
        'password': password,
        'email': changed_email
    }
    
    response = account_api.put_v1_account_email(json_data=json_data)
    
    # Авторизация с измененным имейлом
    
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    
    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 403, 'Пользователь с измененным имейлом авторизован до активации нового токена'
    
    # Получение токена о смене имейла
    token = get_token_by_login(login, response)
    assert token is not None, f'Токен об изменении имейла для пользователя {login} не был получен'
    
    # Активация пользователя с измененным имейлом
    response = account_api.put_v1_account_token(token=token)
    
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'Пользователь с измененным имейлом не был активирован'
    
    # Авторизация пользователя с измененным имейлом
    
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    
    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'Пользователь с новым имейлом не авторизован'
    
def get_token_by_login(login, response):
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



headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0',
}

params = {
    'limit': '50',
}

response = requests.get('http://185.185.143.231:5025/api/v2/messages', params=params, headers=headers, verify=False)