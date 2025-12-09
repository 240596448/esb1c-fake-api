"""Хранилище данных для фейкового API"""
import json
from pathlib import Path
import re
from typing import Dict, Optional, Any


class DataStorage:
    """Хранилище данных в памяти"""
    
    def __init__(self):
        self._clients: Dict[str, Dict[str, Any]] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}
        self._runtime: Dict[str, Dict[str, Any]] = {}
        
        self.repository_token = RepositoryToken()
        self.repository_metadata = RepositoryMetadata()
        self.repository_runtime = RepositoryRuntime()

        self._load_data()

    def _load_data(self):
        """Загрузить данные из репозиториев"""
        self._clients.update(self.repository_token.find())
        self._metadata.update(self.repository_metadata.find())
        self._runtime.update(self.repository_runtime.find())

    def set_token(self, auth_data: tuple[str, str], data: dict):
        """Сохранить данные токена по клиенту"""
        client_id, client_secret = auth_data
        key = client_id
        print(f"set_token: key = {key}")
        
        self._clients[key] = {"data": data, "client_id": client_id, "client_secret": client_secret}
        self.repository_token.save(key, self._clients[key])
        return key
    
    def set_metadata_channels(self, application_name: str, token: str, data: dict):
        """Сохранить metadata каналы по токену"""
        key = f"{application_name}:{token}"
        print(f"set_metadata: key = {key}")
        
        self._metadata[key] = data
        self.repository_metadata.save(key, data)
        return key
    
    def set_runtime_channels(self, application_name: str, token: str, data: dict):
        """Сохранить runtime каналы по токену"""
        key = f"{application_name}:{token}"
        print(f"set_runtime: key = {key}")

        self._runtime[key] = data
        self.repository_runtime.save(key, data)
        return key
    
    def get_token(self, auth_data: tuple[str, str]) -> Optional[dict]:
        """Получить данные токена по клиенту"""
        client_id, client_secret = auth_data
        if client_id not in self._clients:
            raise ValueError(f"Client {client_id} not found")
        token_data = self._clients[client_id]
        if token_data.get("client_secret") != client_secret:
            raise ValueError(f"Invalid client secret for client {client_id}")
        return token_data.get("data")
    
    def get_metadata_channels(self, application_name: str, token: str) -> Optional[dict]:
        """Получить metadata каналы по токену"""
        key = f"{application_name}:{token}"
        print(f"get_metadata: key = {key}, self._metadata = {self._metadata}")
        if key not in self._metadata:
            return None
        return self._metadata[key]
    
    def get_runtime_channels(self, application_name: str, token: str) -> Optional[dict]:
        """Получить runtime каналы по токену"""
        key = f"{application_name}:{token}"
        print(f"get_runtime: key = {key}, self._runtime = {self._runtime}")
        if key not in self._runtime:
            return None
        return self._runtime[key]

class Repository:
    """Репозиторий данных"""
    def __init__(self):
        self.storage_dir = Path("storage")
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.prefix = "unknown_"

    def _write_json_file(self, file_name: str, data: dict):
        """Записать данные в JSON файл"""

        def safe_name(name: str) -> str:
            return re.sub(r'[<>:"/\\|?*]', '_', name)

        clean_path = self.storage_dir / safe_name(file_name)
        with open(clean_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def _read_json_file(self, file_name: str) -> Optional[dict]:
        """Прочитать JSON файл"""
        file_path = self.storage_dir / file_name
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _get_key_data(self, key: str, data: dict) -> str:
        return {"key": key, "data": data}

    def _find_data(self, mask: str) -> Optional[dict]:
        files = self.storage_dir.glob(f"{mask}")
        data: Dict[str, dict] = {}
        for file in files:
            key_data = self._read_json_file(file)
            if key_data:
                key = key_data.get("key")
                data[key] = key_data.get("data")
        return data

    def save(self, key: str, data: dict):
        """Сохранить данные"""
        self._write_json_file(
            f"{self.prefix}{key}.json", 
            self._get_key_data(key, data)
            )

    def find(self) -> Optional[dict]:
        """Найти все данные"""
        return self._find_data(f"{self.prefix}*.json")


class RepositoryToken(Repository):
    """Репозиторий данных токенов"""
    def __init__(self):
        super().__init__()
        self.prefix = "token_"

class RepositoryMetadata(Repository):
    """Репозиторий данных metadata"""
    def __init__(self):
        super().__init__()
        self.prefix = "metadata_"
    
class RepositoryRuntime(Repository):
    """Репозиторий данных runtime"""
    def __init__(self):
        super().__init__()
        self.prefix = "runtime_"
    

storage = DataStorage()

