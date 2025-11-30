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
    
    def set_runtime_channels(self, token: str, data: dict):
        """Сохранить runtime каналы для приложения"""
        if token not in self._tokens:
            self._tokens[token] = {}
        
        self._tokens[token] = data
    
    def get_token(self, auth_data: tuple[str, str]) -> Optional[dict]:
        """Получить данные токена"""
        client_id, client_secret = auth_data
        if client_id not in self._clients:
            raise ValueError(f"Client {client_id} not found")
        data = self._clients[client_id]
        if data.get("client_secret") != client_secret:
            raise ValueError(f"Invalid client secret for client {client_id}")
        return data.get("id_token")
    
    def get_runtime_channels(self, token: str) -> Optional[dict]:
        """Получить runtime каналы"""
        if token not in self._tokens:
            return None
        return self._tokens[token]
    

storage = DataStorage()

