"""
curl -X 'POST' \
  'http://185.185.143.231:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "oops_1",
  "email": "oops_1@mail.ru",
  "password": "oops_1"
}'
"""

# import requests
# import pprint

# url = 'http://185.185.143.231:5051/v1/account'
#
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json'
# }
#
# json = {
#     'login': 'oops_5',
#     'email': 'oops_5@mail.ru',
#     'password': 'oops_5'
# }
#
# response = requests.post(
#     url=url,
#     headers=headers,
#     json=json
# )
#
# print(response.status_code)
# print(response.headers)
#
# 80559209-8a6d-493d-a106-4ef7fb114a50


import requests
import pprint

url = 'http://185.185.143.231:5051/v1/account/80559209-8a6d-493d-a106-4ef7fb114a50'

headers = {
    'accept': 'text/plain'
}

response = requests.put(
    url = url,
    headers = headers
)


print(response.status_code)
print(response.json())