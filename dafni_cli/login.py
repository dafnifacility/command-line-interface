import requests
from dafni_cli.urls import LOGIN_API_URL
from json.decoder import JSONDecodeError


def login(username: str, password: str) -> str:
    login_resp = requests.post(
        LOGIN_API_URL,
        {
            "username": username,
            "password": password,
            "client_id": "dafni-main",
            "grant_type": "password",
            "scope": "openid",
        },
    )
    try:
        access_token = login_resp.json()["access_token"]
        return f"Bearer {access_token}"
    except (KeyError, AttributeError, JSONDecodeError) as e:
        print(f"Login failed with {e}")
        return None
