import requests

endpoint = 'http://127.0.0.1:8000/api/tasks/1/update/'

data = {
    "title": "Reading",
}

get_response = requests.put(endpoint, json=data)

print(get_response.json())