import requests

class AccountApi:
    def __init__(
            self,
            host,
            headers=None
        ):
        self.host = host
        self.headers = headers
    
    def post_v1_account(
            self,
            json_data
            ):
        """
                Register new user

        :param json_data:
        :return:
        """
        response = requests.post(
            url=f'{self.host}/v1/account',
            json=json_data
        )
        return response
    
    def put_v1_account_token(
            self,
            token
            ):
        """
        Activate registered user
        :param token:
        :return:
        """
        response = requests.put(
            url=f'{self.host}/v1/account/{token}',
        )
        print(response.status_code)
        print(response.text)
        assert response.status_code == 200, 'Пльзователь не активирован'
        return response
    def put_v1_account_email(
            self,
            json_data
            ):
        """
        Change registered user email
        :param json_data:
        :return:
        """
        response = requests.put(
            url = f'{self.host}/v1/account/email',
            json=json_data
        )
        
        print(response.status_code)
        print(response.text)
        assert response.status_code == 200, 'Email не изменен'
        return response