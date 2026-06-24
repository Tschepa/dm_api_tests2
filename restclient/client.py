# пакет - модуль - класс (те же параметры, что и у апишек)

from requests import session
import structlog
import uuid
from json import JSONDecodeError


class RestClient:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers
        self.session = session() # иниц-ия сессии
        # иниц-я логгер с именем текущего модуля и добавь во все сообщения поле service='api', чтобы я знал, откуда пришёл лог.
        self.log = structlog.get_logger(__name__).bind(service='api')# иниц-ия логов
        
    def post(
            self,
            path,
            **kwargs
    ):
        return self._send_request(method='POST', path=path, **kwargs)
    
    def get(
            self,
            path,
            **kwargs
    ):
        return self._send_request(method='GET', path=path, **kwargs)
    
    def put(
            self,
            path,
            **kwargs
    ):
        return self._send_request(method='PUT', path=path, **kwargs)
    
    def delete(
            self,
            path,
            **kwargs
    ):
        return self._send_request(method='DELETE', path=path, **kwargs)
    
    # метод, логирующий запросы (тип мет., эндпойнт, аргументы, с которыми может работать библиотека requests)
    def _send_request(self, method, path, **kwargs):
        # pip install structlog =>  фиксируем зависимости pip freeze > requirements.txt
        log = self.log.bind(event_id=str(uuid.uuid4()))
        full_url= self.host + path
        
        # логируем запрос
        log.msg(
            event='Request',
            method=method,
            full_url=full_url,
            params=kwargs.get('params'),
            headers=kwargs.get('headers'),
            json=kwargs.get('json'),
            data=kwargs.get('data')
        )
        # выполняем запрос
        rest_response = self.session.request(method=method, url=full_url, **kwargs)
        
        # логирование ответа сервера
        log.msg(
            event='Response',
            status_code=rest_response.status_code,
            headers=rest_response.headers,
            #json=rest_response.json()
            json=self._get_json(rest_response)
        )
        return rest_response
    
    # при регистрации в ответе нет тела, обходим этот кейс
    @staticmethod
    def _get_json(rest_response):
        try:
            return rest_response.json()
        except JSONDecodeError:
            return{}