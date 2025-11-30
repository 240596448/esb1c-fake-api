"""Хранилище данных для фейкового API"""
from typing import Dict, Optional, Any


class DataStorage:
    """Хранилище данных по application_name"""
    
    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = {}
        self._client_id_index: Dict[str, str] = {}  # client_id -> application_name
    
    def set_token(self, application_name: str, data: dict):
        """Сохранить данные токена для приложения"""
        if application_name not in self._storage:
            self._storage[application_name] = {}
        
        key = data.get("client_id")
        self._storage[application_name][key] = data
    
    def set_runtime_channels(self, application_name: str, runtime_channels: dict):
        """Сохранить runtime каналы для приложения"""
        if application_name not in self._storage:
            self._storage[application_name] = {}
        
        self._storage[application_name]["runtime_channels"] = runtime_channels
    
    def get_token(self, application_name: str) -> Optional[dict]:
        """Получить данные токена"""
        if application_name not in self._storage:
            return None
        return self._storage[application_name].get("token")
    
    def get_runtime_channels(self, application_name: str) -> Optional[dict]:
        """Получить runtime каналы"""
        if application_name not in self._storage:
            return None
        return self._storage[application_name].get("runtime_channels")
    
    def has_application(self, application_name: str) -> bool:
        """Проверить наличие данных для приложения"""
        return application_name in self._storage


storage = DataStorage()

