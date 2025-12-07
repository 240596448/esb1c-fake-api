"""Модели данных для ESB API"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, RootModel

# Модели для раздельных файлов конфигурации
class MetadataChannel(BaseModel):
    """Канал метаданных"""
    process: str
    processDescription: Optional[str] = Field(default="")
    channel: str
    channelDescription: Optional[str] = Field(default="")
    access: Literal["READ_ONLY", "WRITE_ONLY"]

class MetadataChannels(RootModel[List[MetadataChannel]]):
    """Список метаданных каналов"""
    root: List[MetadataChannel]

class RuntimeChannel(BaseModel):
    """Runtime канал"""
    process: str
    channel: str
    destination: str

class RuntimeChannels(BaseModel):
    """Список runtime каналов"""
    items: List[RuntimeChannel]
    port: int

class Token(BaseModel):
    """Токен"""
    id_token: str
    token_type: str = Field(default="Bearer")
    access_token: str = Field(default="Not implemented")

class ClientInfo(BaseModel):
    """Конфигурация клиента"""
    application_name: str
    client_id: str
    client_secret: str


# Модели для конфигурации приложения одним файлом
class ChannelConfig(BaseModel):
    """Конфигурация канала"""
    channel: str
    channelDescription: Optional[str] = Field(default="")
    access: Literal["READ_ONLY", "WRITE_ONLY"]
    destination: Optional[str] = Field(default=None)

class ProcessConfig(BaseModel):
    """Конфигурация процесса"""
    process: str
    processDescription: Optional[str] = Field(default="")
    channels: List[ChannelConfig]

class ApplicationConfig(BaseModel):
    """Данные приложения"""
    application_name: str
    client_id: str
    client_secret: str
    id_token: str
    port: int
    processes: List[ProcessConfig]
