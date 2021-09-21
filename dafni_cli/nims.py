import requests
from pathlib import Path
from dafni_cli.urls import MODELS_API_URL
from requests import Response
from typing import Optional
from json.decoder import JSONDecodeError


class NIMSError(Exception):
    def __init__(self, prefix: str, response: Response):
        self.prefix = prefix
        self.response = response

    @property
    def status_code(self):
        return self.response.status_code

    @property
    def response_text(self):
        try:
            return self.response.json()
        except JSONDecodeError:
            return self.response.text

    @property
    def message(self):
        message = self.prefix + f" failed with status code {self.status_code}"
        if self.response_text is not None:
            message += f" and response: {self.response_text}"
        return message


def validate_model_definition(
    jwt: str, model_definition: Path
) -> tuple[bool, list[str]]:
    validation_headers = {"Authorization": jwt, "Content-Type": "application/yaml"}
    with model_definition.open("rb") as md:
        validation_resp = requests.put(
            f"{MODELS_API_URL}/models/validate/",
            data=md,
            headers=validation_headers,
        )
        try:
            if not validation_resp.json()["valid"]:
                return False, validation_resp.json()["errors"]
        except (KeyError, JSONDecodeError) as e:
            raise NIMSError("Validation", validation_resp)
    return True, []


def get_model_upload_urls(
    jwt: str, image: bool = True, definition: bool = True
) -> tuple[str, dict]:
    auth_header = {"Authorization": jwt}
    urls_resp = requests.post(
        f"{MODELS_API_URL}/models/upload/",
        headers=auth_header,
        json={"image": True, "definition": True},
    )
    if urls_resp.status_code != 200:
        raise NIMSError("Getting upload URLs", urls_resp)
    upload_id = urls_resp.json()["id"]
    urls = urls_resp.json()["urls"]
    return upload_id, urls


def upload_file_to_minio(jwt: str, url: str, file_path: Path) -> None:
    upload_headers = {"Authorization": jwt, "Content-Type": "multipart/form-data"}
    with file_path.open("rb") as file_data:
        response = requests.put(url, headers=upload_headers, data=file_data)
        if response.status_code != 200:
            raise NIMSError("Uploading to Minio", response)


def ingest_model(
    jwt: str, upload_id: str, version_message: str, model_id: Optional[str] = None
) -> None:
    endpoint = f"{MODELS_API_URL}/models/upload/{upload_id}/ingest/"
    if model_id:
        endpoint = f"{MODELS_API_URL}/models/{model_id}/upload/{upload_id}/ingest/"
    auth_header = {"Authorization": jwt}
    response = requests.post(
        endpoint,
        headers=auth_header,
        json={"version_message": version_message},
    )
    if response.status_code != 200:
        raise NIMSError("Model ingest", response)
