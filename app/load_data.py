"""Скрипт для загрузки данных из JSON файлов"""
import json
import requests
import sys
from pathlib import Path


def load_token(application_name: str = None, base_url: str = "http://localhost:5000"):
    """Загрузить данные токена из get_token.json"""
    data_dir = Path(__file__).parent.parent / "data"
    token_file = data_dir / "get_token.json"
    
    with open(token_file, 'r', encoding='utf-8') as f:
        token_data = json.load(f)
    
    # Используем application_name из token_data, если не передан явно
    if not application_name:
        application_name = token_data.get("application_name")
        if not application_name:
            raise ValueError("application_name must be provided either as argument or in get_token.json")
    
    payload = {
        "application_name": application_name,
        "token": token_data
    }
    
    response = requests.post(f"{base_url}/setup/token", json=payload)
    response.raise_for_status()
    
    print(f"Токен для приложения '{application_name}' успешно загружен")
    return response.json()


def load_runtime_channels(application_name: str = None, base_url: str = "http://localhost:5000"):
    """Загрузить runtime каналы из get_runtime_channels.json"""
    data_dir = Path(__file__).parent.parent / "data"
    runtime_channels_file = data_dir / "get_runtime_channels.json"
    
    with open(runtime_channels_file, 'r', encoding='utf-8') as f:
        runtime_channels = json.load(f)
    
    # Используем application_name из get_token.json, если не передан явно
    if not application_name:
        token_file = data_dir / "get_token.json"
        with open(token_file, 'r', encoding='utf-8') as f:
            token_data = json.load(f)
        application_name = token_data.get("application_name")
        if not application_name:
            raise ValueError("application_name must be provided either as argument or in get_token.json")
    
    payload = {
        "application_name": application_name,
        "runtime_channels": runtime_channels
    }
    
    response = requests.post(f"{base_url}/setup/runtime_channels", json=payload)
    response.raise_for_status()
    
    print(f"Runtime каналы для приложения '{application_name}' успешно загружены")
    return response.json()


if __name__ == '__main__':
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    
    try:
        load_token(base_url=base_url)
        load_runtime_channels(base_url=base_url)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

