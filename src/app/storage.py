"""Хранилище данных для фейкового API"""
from typing import Dict, Optional, Any


class DataStorage:
    """Хранилище данных в памяти"""
    
    def __init__(self):
        self._tokens: Dict[str, Dict[str, Any]] = {}
        self._clients: Dict[str, Dict[str, Any]] = {}


    def set_token(self, auth_data: tuple[str, str], data: dict):
        """Сохранить данные токена по клиенту"""
        client_id, client_secret = auth_data
        key = client_id
        print(f"key: {key}")
        if key not in self._clients:
            self._clients[key] = {}
        
        self._clients[key] = {**data, "client_id": client_id, "client_secret": client_secret}
        return key
    
    def set_metadata_channels(self, application_name: str, token: str, data: dict):
        """Сохранить metadata каналы по токену"""
        key = f"{application_name}:{token}"
        print(f"key: {key}")
        if key not in self._tokens:
            self._tokens[key] = {}
        
        self._tokens[key]["metadata_channels"] = data
        return key
    
    def set_runtime_channels(self, application_name: str, token: str, data: dict):
        """Сохранить runtime каналы по токену"""
        key = f"{application_name}:{token}"
        print(f"key: {key}")
        if key not in self._tokens:
            self._tokens[key] = {}
        
        self._tokens[key]["runtime_channels"] = data
        return key
    
    def get_token(self, auth_data: tuple[str, str]) -> Optional[dict]:
        """Получить данные токена по клиенту"""
        client_id, client_secret = auth_data
        if client_id not in self._clients:
            raise ValueError(f"Client {client_id} not found")
        data = self._clients[client_id]
        if data.get("client_secret") != client_secret:
            raise ValueError(f"Invalid client secret for client {client_id}")
        return {
            "id_token": data.get("id_token"),
            "token_type": data.get("token_type"),
            "access_token": data.get("access_token")
        }
    
    def get_metadata_channels(self, application_name: str, token: str) -> Optional[dict]:
        """Получить metadata каналы по токену"""
        key = f"{application_name}:{token}"
        print(f"key: {key}")
        if key not in self._tokens:
            return None
        return self._tokens[key].get("metadata_channels")
    
    def get_runtime_channels(self, application_name: str, token: str) -> Optional[dict]:
        """Получить runtime каналы по токену"""
        key = f"{application_name}:{token}"
        print(f"key: {key}")
        if key not in self._tokens:
            return None
        return self._tokens[key].get("runtime_channels")

storage = DataStorage()

