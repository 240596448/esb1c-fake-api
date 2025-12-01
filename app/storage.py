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
        if key not in self._clients:
            self._clients[key] = {}
        
        self._clients[key] = {**data, "client_id": client_id, "client_secret": client_secret}
    
    def set_metadata_channels(self, token: str, data: dict):
        """Сохранить metadata каналы по токену"""
        if token not in self._tokens:
            self._tokens[token] = {}
        
        self._tokens[token]["metadata_channels"] = data
    
    def set_runtime_channels(self, token: str, data: dict):
        """Сохранить runtime каналы по токену"""
        if token not in self._tokens:
            self._tokens[token] = {}
        
        self._tokens[token]["runtime_channels"] = data
    
    def get_token(self, auth_data: tuple[str, str]) -> Optional[dict]:
        """Получить данные токена по клиенту"""
        client_id, client_secret = auth_data
        if client_id not in self._clients:
            raise ValueError(f"Client {client_id} not found")
        data = self._clients[client_id]
        if data.get("client_secret") != client_secret:
            raise ValueError(f"Invalid client secret for client {client_id}")
        return data.get("id_token")
    
    def get_metadata_channels(self, token: str) -> Optional[dict]:
        """Получить metadata каналы по токену"""
        if token not in self._tokens:
            return None
        return self._tokens[token].get("metadata_channels")
    
    def get_runtime_channels(self, token: str) -> Optional[dict]:
        """Получить runtime каналы по токену"""
        return self._tokens[token].get("runtime_channels")

storage = DataStorage()

