"""Хранилище данных для фейкового API"""
from typing import Dict, Optional, Any


class DataStorage:
    """Хранилище данных по application_name"""
    
    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = {}
    
    def set_data(self, application_name: str, token_data: dict, metadata: list, runtime_channels: dict):
        """Сохранить данные для приложения"""
        self._storage[application_name] = {
            "token": token_data,
            "metadata": metadata,
            "runtime_channels": runtime_channels
        }
    
    def get_token(self, application_name: str) -> Optional[dict]:
        """Получить данные токена"""
        if application_name not in self._storage:
            return None
        return self._storage[application_name].get("token")
    
    def get_metadata(self, application_name: str) -> Optional[list]:
        """Получить метаданные каналов"""
        if application_name not in self._storage:
            return None
        return self._storage[application_name].get("metadata")
    
    def get_runtime_channels(self, application_name: str) -> Optional[dict]:
        """Получить runtime каналы"""
        if application_name not in self._storage:
            return None
        return self._storage[application_name].get("runtime_channels")
    
    def has_application(self, application_name: str) -> bool:
        """Проверить наличие данных для приложения"""
        return application_name in self._storage


storage = DataStorage()

