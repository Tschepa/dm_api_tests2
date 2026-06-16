import requests
import pprint
from json import loads
def test_v1_account():
    # Регистрация пользователя

    login = 'wow3'
    email = f'{login}@mail.ru'
    password = '12345678'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://185.185.143.231:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f'Польователь не был создан, {response.json()}'

    # Получение письма в почтовом сервере

    params = {
        'limit': '50',
    }

    response = requests.get('http://185.185.143.231:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)
    # pprint.pprint(response.json())
    # Получение токена
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(user_login)
            print(token)
            assert token is not None, 'Письмо с токеном не пришло'
    # Активация пользователя
    response = requests.put(f'http://185.185.143.231:5051/v1/account/{token}')
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'Пльзователь не активирован'
    # Авторизация пользователя

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://185.185.143.231:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'Пользователь не авторизован'