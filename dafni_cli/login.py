import requests
from dafni_cli.urls import LOGIN_API_URL


def login(username: str, password: str) -> str:
    login_resp = requests.post(
        f"{LOGIN_API_URL}/login/",
        json={"username": username, "password": password},
        headers={
            "Content-Type": "application/json",
        },
        allow_redirects=False,
    )
    login_resp.raise_for_status()
    return f"JWT {login_resp.cookies['__Secure-dafnijwt']}"
