import requests


def test_v1_account():
    # Регистрация пользователя

    # headers = {
    #     'accept': '*/*',
    #     'Content-Type': 'application/json',
    # }
    login = 'test1'
    email = f'{login}@mail.ru'
    password = 'test123'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://185.185.143.231:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)

    # Получение письма в почтовом сервере
    # headers = {
    #     'Accept': 'application/json, text/plain, */*',
    #     'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    #     'Cache-Control': 'no-cache',
    #     'Connection': 'keep-alive',
    #     'Pragma': 'no-cache',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0',
    # }

    params = {
        'limit': '50',
    }

    response = requests.get('http://185.185.143.231:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)
    # Получение токена

    # Активация пользователя
    # headers = {
    #     'accept': 'text/plain',
    # }

    response = requests.put('http://185.185.143.231:5051/v1/account/45339a17-c566-4fd9-93a9-56082230de12')
    print(response.status_code)
    print(response.text)
    # Авторизация пользователя
    # headers = {
    #     'accept': 'text/plain',
    #     'Content-Type': 'application/json',
    # }

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://185.185.143.231:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
