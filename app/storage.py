"""Хранилище данных для фейкового API"""
from typing import Dict, Optional, Any


class DataStorage:
    """Хранилище данных по application_name"""
    
    def __init__(self):
        self._tokens: Dict[str, Dict[str, Any]] = {}
        self._clients: Dict[str, Dict[str, Any]] = {}

    def set_token(self, auth_data: tuple[str, str], data: dict):
        """Сохранить данные токена для клиента"""
        client_id, client_secret = auth_data
        key = client_id
        if key not in self._clients:
            self._clients[key] = {}
        
        self._clients[key] = {**data, "client_id": client_id, "client_secret": client_secret}
    
    def set_runtime_channels(self, data: dict):
        """Сохранить runtime каналы для приложения"""
        if application_name not in self._storage:
            self._storage[application_name] = {}
        
        key = self._storage.get("application_name")
        self._storage[application_name]["runtime_channels"] = runtime_channels
    
    def get_token(self, auth_data: tuple[str, str]) -> Optional[dict]:
        """Получить данные токена"""
        client_id, client_secret = auth_data
        if client_id not in self._clients:
            raise ValueError(f"Client {client_id} not found")
        data = self._clients[client_id]
        if data.get("client_secret") != client_secret:
            raise ValueError(f"Invalid client secret for client {client_id}")
        return data.get("id_token")
    
    def get_runtime_channels(self, application_name: str) -> Optional[dict]:
        """Получить runtime каналы"""
        if application_name not in self._storage:
            return None
        return self._storage[application_name].get("runtime_channels")
    
    def has_application(self, application_name: str) -> bool:
        """Проверить наличие данных для приложения"""
        return application_name in self._storage


storage = DataStorage()

