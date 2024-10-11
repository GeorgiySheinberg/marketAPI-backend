import requests

url = 'http://127.0.0.1:8000/update/'

fp = open('shop1.yaml', 'rb')
file = {'file': fp}
token = "9991c9669875eb9d5c3da7dd8b225384ef6bb9e6"


response = requests.post(url, headers={"Authorization": f'Token {token}'}, files=file)
print(response.text)
print(response.status_code)
