"""Скрипт для загрузки данных из JSON файлов"""
import json
import requests
import sys
from pathlib import Path


def load_data(application_name: str, base_url: str = "http://localhost:5000"):
    """Загрузить данные из JSON файлов в фейковый API"""
    data_dir = Path(__file__).parent.parent / "data"
    
    token_file = data_dir / "get_token.json"
    metadata_file = data_dir / "get_metadata.json"
    runtime_channels_file = data_dir / "get_runtime_channels.json"
    
    with open(token_file, 'r', encoding='utf-8') as f:
        token_data = json.load(f)
    
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    with open(runtime_channels_file, 'r', encoding='utf-8') as f:
        runtime_channels = json.load(f)
    
    payload = {
        "application_name": application_name,
        "token": token_data,
        "metadata": metadata,
        "runtime_channels": runtime_channels
    }
    
    response = requests.post(f"{base_url}/setup", json=payload)
    response.raise_for_status()
    
    print(f"Данные для приложения '{application_name}' успешно загружены")
    return response.json()


if __name__ == '__main__':
    app_name = sys.argv[1] if len(sys.argv) > 1 else "test_app"
    base_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:5000"
    
    try:
        load_data(app_name, base_url)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

