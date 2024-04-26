import requests
from getpass import getpass

from dataclasses import dataclass
import pathlib
import json

"""
endpoint = 'http://127.0.0.1:8000/api/auth/'
username = input("Enter your username\n")
password = getpass("Enter your password\n")

auth_response = requests.post(endpoint, json={"username": username, "password": password})

if auth_response.status_code == 200:
    token = auth_response.json()["token"]
    headers = {
        "Authorization": f"Bearer {token}"
    }
    endpoint = 'http://127.0.0.1:8000/api/tasks/'

    get_response = requests.get(endpoint, headers=headers)
    print(get_response.json())
else:
    raise Exception("Invalid username or password")
"""


# Simple JWT
@dataclass
class JWTClient:
    access:str = None
    refresh:str = None
    header_type:str = "Bearer"
    base_endpoint = 'http://127.0.0.1:8000/api'
    file_path: pathlib.Path = pathlib.Path('jwt_token.json')

    def __post_init__(self):
        if self.file_path.exists():
            try:
                data = json.loads(self.file_path.read_text())
            except Exception:
                # if data is tampered with
                data = None
            if data is None:
                self.clear_tokens()
                self.perform_auth()
            else:
                self.access = data.get('access')
                self.refresh = data.get('refresh')
                token_verified = self.verify_token()
                if not token_verified:
                    # invalid or expired token
                    refreshed = self.perform_refresh()
                    if not refreshed:
                        # token refresh fail
                        print("Invalid data, login again")
                        self.clear_tokens()
                        self.perform_auth()
        else:
            self.perform_auth()

    def get_headers(self, header_type=None):
        _type = header_type or self.header_type
        token =self.access
        if not token:
            return {}
        return {
            "Authorization": f"{_type} {token}"
        }

    def write_token(self, data:dict):
        # perform authentication without exposing password
        if self.file_path is not None:
            self.access = data.get('access')
            self.refresh = data.get('refresh')
            if self.access and self.refresh:
                self.file_path.write_text(json.dumps(data))

    def perform_auth(self):
        endpoint = f"{self.base_endpoint}/token/"
        username = input("Enter your username:\n")
        password = getpass("Enter your password:\n")
        response = requests.post(endpoint, json={'username': username, 'password': password})
        if response.status_code != 200:
            raise Exception(f"Access not granted: {response.text}")
        print("Access granted")
        self.write_token(response.json())

    def verify_token(self):
        data = {
            "token": f"{self.access}"
        }
        endpoint = f"{self.base_endpoint}/token/verify/"
        response = requests.post(endpoint, json=data)
        return response.status_code == 200

    def clear_tokens(self):
        self.access = None
        self.refresh = None
        if self.file_path.exists():
            self.file_path.unlink()

    def perform_refresh(self):
        print("Token expired!!!\n Refresh token...")
        headers = self.get_headers()
        data = {
            "refresh": f"{self.refresh}"
        }
        endpoint = f"{self.base_endpoint}/token/refresh/"
        response = requests.post(endpoint, json=data, headers=headers)
        if response.status_code != 200:
            self.clear_tokens()
            return False
        refresh_data = response.json()
        if not 'access' in refresh_data:
            self.clear_tokens()
            return False
        stored_data = {
            'access': refresh_data.get('access'),
            'refresh': self.refresh
        }
        self.write_token(stored_data)
        return True


    def list(self, endpoint=None, limit=3):
        # api call to DRF view which require simpleJWT authentication
        headers = self.get_headers()
        if endpoint is None or self.base_endpoint not in str(endpoint):
            endpoint = f"{self.base_endpoint}/tasks/?limit={limit}"
        response = requests.get(endpoint, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Request not complete {response.text}")
        data = response.json()
        return data


if __name__ == "__main__":
    client = JWTClient()
    lookup_data_1 = client.list(limit=5)
    results = lookup_data_1.get('results')
    next_url = lookup_data_1.get('next')
    print(results)
    if next_url:
        lookup_data_2 = client.list(endpoint=next_url)
        results += lookup_data_2.get('results')
        print(results)


