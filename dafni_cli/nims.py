import requests
from pathlib import Path
from dafni_cli.urls import MODELS_API_URL


def validate_model_definition(
    jwt: str, model_definition: Path
) -> tuple[bool, list[str]]:
    validation_headers = {"Authorization": jwt, "Content-Type": "application/yaml"}
    with model_definition.open("rb") as md:
        validation_resp = requests.put(
            f"{MODELS_API_URL}/models/definition/validate/",
            headers=validation_headers,
            data=md,
        )
        validation_resp.raise_for_status()
        if not validation_resp.json()["valid"]:
            return False, validation_resp.json()["errors"]
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
    urls_resp.raise_for_status()
    upload_id = urls_resp.json()["id"]
    urls = urls_resp.json()["urls"]
    return upload_id, urls


def upload_file_to_minio(jwt: str, url: str, file_path: Path) -> None:
    upload_headers = {"Authorization": jwt, "Content-Type": "multipart/form-data"}
    with file_path.open("rb") as file_data:
        requests.put(url, headers=upload_headers, data=file_data)


def start_model_ingest(jwt: str, upload_id: str, version_message: str):
    auth_header = {"Authorization": jwt}
    ingest_resp = requests.post(
        f"{MODELS_API_URL}/models/upload/{upload_id}/ingest/",
        headers=auth_header,
        json={"version_message": version_message},
    )
    ingest_resp.raise_for_status()


def start_model_version_ingest(
    jwt: str, model_id: str, upload_id: str, version_message: str
):
    auth_header = {"Authorization": jwt}
    ingest_resp = requests.post(
        f"{MODELS_API_URL}/models/{model_id}/upload/{upload_id}/ingest/",
        headers=auth_header,
        json={"version_message": version_message},
    )
    ingest_resp.raise_for_status()
