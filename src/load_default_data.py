"""Скрипт для загрузки данных из JSON файлов"""

import json
import sys
from pathlib import Path
import requests

data_dir = Path(__file__).parent.parent / "data" / "example-esb-answer"

def load_token(url: str, client_id: str, client_secret: str):
    """Загрузить данные токена из get_token.json"""
    token_file = data_dir / "get_token.json"
    token_file_data = json.loads(token_file.read_text(encoding="utf-8"))

    response = requests.post(
        f"{url}/setup/token",
        auth=(client_id, client_secret),
        json=token_file_data,
        timeout=10,
    )
    response.raise_for_status()

    print(f"Данные токена пользователя '{client_id}' успешно загружены")
    return response.json()

def load_metadata_channels(url: str, application_name: str, token: str):
    """Загрузить metadata каналы из get_metadata_channels.json"""
    metadata_file = data_dir / "get_metadata.json"
    metadata = json.loads(metadata_file.read_text(encoding="utf-8"))

    response = requests.post(
        f"{url}/setup/metadata_channels",
        json=metadata,
        headers={
            "Authorization": f"Bearer {token}", 
            "x-fake-application-name": application_name
            },
        timeout=10,
    )
    response.raise_for_status()

    print(f"Metadata каналы успешно загружены: {application_name}:{token}")
    return response.json()


def load_runtime_channels(url: str, application_name: str, token: str):
    """Загрузить runtime каналы из get_runtime_channels.json"""
    runtime_channels_file = data_dir / "get_runtime_channels.json"
    runtime_channels = json.loads(runtime_channels_file.read_text(encoding="utf-8"))

    response = requests.post(
        f"{url}/setup/runtime_channels",
        json=runtime_channels,
        headers={
            "Authorization": f"Bearer {token}", 
            "x-fake-application-name": application_name
        },
        timeout=10,
        )
    response.raise_for_status()

    print(f"Runtime каналы успешно загружены: {application_name}:{token}")
    return response.json()


if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    print(f"Загружаем данные в {base_url}")

    client_file = data_dir / "client.json"
    if not client_file.exists():
        print(f"Файл {client_file} не найден")
        sys.exit(1)
    try:
        client_data = json.loads(client_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Ошибка загрузки данных из файла {client_file}: {e}")
        sys.exit(1)

    try:
        token_data = load_token(
            url=base_url,
            client_id=client_data["client_id"],
            client_secret=client_data["client_secret"])
        metadata_channels_data = load_metadata_channels(
            url=base_url,
            application_name=client_data["application_name"],
            token=token_data["value"]["id_token"])
        runtime_channels_data = load_runtime_channels(url=base_url,
            application_name=client_data["application_name"],
            token=token_data["value"]["id_token"])
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        sys.exit(1)
