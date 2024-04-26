import requests


# auth_endpoint = 'http://127.0.0.1:8000/api/auth/'    # Basic Auth
auth_endpoint = 'http://127.0.0.1:8000/api/token/'      # JWT
auth_response = requests.post(auth_endpoint, json={'username': 'jubril', 'password': 'jubril'})
# token = auth_response.json()['token']
token = auth_response.json()['access']
# token = auth_response.json()
# print(token)

headers = {
    "Authorization": f"Bearer {token}"
}

endpoint = 'http://127.0.0.1:8000/api/tasks/'

get_response = requests.get(endpoint, headers=headers)

print(get_response.json())
