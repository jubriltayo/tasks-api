import requests


auth_endpoint = 'http://127.0.0.1:8000/api/token/'      # JWT
auth_response = requests.post(auth_endpoint, json={'username': 'jubril', 'password': 'jubril'})
token = auth_response.json()['access']
print(token)


headers = {
    # "Authorization": "Bearer 51c25ba746588ab10a3f884f5c3a222f77c57d4d"
    "Authorization": f"Bearer {token}"
}

endpoint = 'http://127.0.0.1:8000/api/tasks/'

data = {
    "title": "Singing",
    "completed": True
}

get_response = requests.post(endpoint, json=data, headers=headers)

print(get_response.json())