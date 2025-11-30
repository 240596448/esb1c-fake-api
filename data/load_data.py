"""Скрипт для загрузки данных из JSON файлов"""

import json
import requests
import sys
from pathlib import Path


def load_token(client_id: str, client_secret: str, base_url: str = "http://localhost:5000"):
    """Загрузить данные токена из get_token.json"""
    data_dir = Path(__file__).parent
    token_file = data_dir / "get_token.json"
    token_data = json.loads(token_file.read_text(encoding="utf-8"))

    response = requests.post(
        f"{base_url}/setup/token",
        auth=(client_id, client_secret),
        json=token_data,
    )
    response.raise_for_status()

    print(f"Данные токена пользователя '{client_id}' успешно загружены")
    return response.json()


def load_runtime_channels(base_url: str = "http://localhost:5000", token: str = None
):
    """Загрузить runtime каналы из get_runtime_channels.json"""
    data_dir = Path(__file__).parent
    runtime_channels_file = data_dir / "get_runtime_channels.json"
    runtime_channels = json.loads(runtime_channels_file.read_text(encoding="utf-8"))

    response = requests.post(
        f"{base_url}/setup/runtime_channels",
        json=runtime_channels,
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()

    print(f"Runtime каналы для токена '{token}' успешно загружены")
    return response.json()


if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    client_data = json.loads(Path(__file__).parent / "client.json")
    client_id = client_data["client_id"]
    client_secret = client_data["client_secret"]

    try:
        token_data = load_token(base_url=base_url, client_id=client_id, client_secret=client_secret)
        print(f"Данные токена пользователя '{client_id}' успешно загружены")
    
        runtime_channels_data = load_runtime_channels(base_url=base_url, token=token_data["value"]["id_token"])
        print(f"Runtime каналы успешно загружены")
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
