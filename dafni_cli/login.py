import requests
from dafni_cli.urls import LOGIN_API_URL
from json.decoder import JSONDecodeError


def login(username: str, password: str) -> str:
    login_resp = requests.post(
        f"{LOGIN_API_URL}/login/",
        json={"username": username, "password": password},
        headers={
            "Content-Type": "application/json",
        },
        allow_redirects=False,
    )
    try:
        return f"JWT {login_resp.cookies['__Secure-dafnijwt']}"
    except (KeyError, AttributeError, JSONDecodeError) as e:
        print(f"Login failed with {e}")
        return None
    

