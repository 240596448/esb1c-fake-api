from pathlib import Path
import requests
from app.models import (
    ApplicationConfig,
    MetadataChannels, MetadataChannel,
    RuntimeChannels, RuntimeChannel,
    ClientInfo, Token,
)


class SingleConfig:
    def __init__(self, file_path: str):
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} not found")
        self.application_config = self._load_data(file_path)

    def _load_data(self, file_path: Path) -> ApplicationConfig:
        data = file_path.read_text(encoding="utf-8")
        return ApplicationConfig.model_validate_json(data)

    def client_info(self) -> ClientInfo:
        """Получить информацию о клиенте"""
        return ClientInfo(**self.application_config.model_dump())

    def get_token(self) -> Token:
        """Получить ответ на запрос токена"""
        return Token(id_token=self.application_config.id_token)

    def get_channels(self) -> MetadataChannels:
        """Получить ответ на запрос метаданных каналов"""

        channels = []
        for process in self.application_config.processes:
            for channel in process.channels:
                md_channel = MetadataChannel(
                    process=process.process,
                    processDescription=process.processDescription,
                    channel=channel.channel,
                    channelDescription=channel.channelDescription,
                    access=channel.access)
                channels.append(md_channel)
        return MetadataChannels(root=channels)

    def get_runtime_channels(self) -> RuntimeChannels:
        """Получить ответ на запрос runtime каналов"""
        channels = []
        for process in self.application_config.processes:
            for channel in process.channels:
                rt_channel = RuntimeChannel(
                    process=process.process,
                    channel=channel.channel,
                    destination=channel.destination)
                channels.append(rt_channel)
        return RuntimeChannels(items=channels, port=self.application_config.port)


class MultiConfig:
    def __init__(self, dir_path: str):
        dir_path = Path(dir_path)
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory {dir_path.absolute()} not found (data directory)")
        self.dir_path = dir_path
        self.client = self._load_client_info()
        self.token = self._load_token()
        self.metadata = self._load_metadata()
        self.runtime = self._load_runtime()

    def _load_client_info(self) -> ClientInfo:
        client_configs = self.dir_path / "client.json"
        if not client_configs.exists():
            raise FileNotFoundError(f"File {client_configs} not found (client.json)")
        data = client_configs.read_text()
        return ClientInfo.model_validate_json(data)

    def _load_token(self) -> Token:
        token_configs = self.dir_path / "get_token.json"
        if not token_configs.exists():
            raise FileNotFoundError(f"File {token_configs} not found (get_token.json)")
        data = token_configs.read_text()
        return Token.model_validate_json(data)

    def _load_metadata(self) -> MetadataChannels:
        metadata_configs = self.dir_path / "get_metadata.json"
        if not metadata_configs.exists():
            raise FileNotFoundError(f"File {metadata_configs} not found (get_metadata.json)")
        data = metadata_configs.read_text(encoding="utf-8")
        return MetadataChannels.model_validate_json(data)

    def _load_runtime(self) -> RuntimeChannels:
        runtime_configs = self.dir_path / "get_runtime_channels.json"
        if not runtime_configs.exists():
            raise FileNotFoundError(f"File {runtime_configs} not found (get_runtime_channels.json)")
        data = runtime_configs.read_text()
        return RuntimeChannels.model_validate_json(data)

    def client_info(self) -> ClientInfo:
        """Получить информацию о клиенте"""
        return self.client

    def get_token(self) -> Token:
        """Получить ответ на запрос токена"""
        return self.token

    def get_channels(self) -> MetadataChannels:
        """Получить ответ на запрос метаданных каналов"""
        return self.metadata

    def get_runtime_channels(self) -> RuntimeChannels:
        """Получить ответ на запрос runtime каналов"""
        return self.runtime


class ApplicationLoader:
    def __init__(self, config: SingleConfig | MultiConfig, url: str):
        self.url = url
        self.client_info: ClientInfo = config.client_info()
        self.token: Token = config.get_token()
        self.metadata: MetadataChannels = config.get_channels()
        self.runtime: RuntimeChannels = config.get_runtime_channels()

    def load_token(self):
        """Загрузить данные токена из get_token.json"""
        response = requests.post(
            f"{self.url}/setup/token",
            auth=(self.client_info.client_id, self.client_info.client_secret),
            json=self.token.model_dump(),
            timeout=10,
        )
        response.raise_for_status()
        print(f"Данные токена пользователя '{self.client_info.client_id}' успешно загружены")

    def load_metadata(self):
        """Загрузить metadata каналы из get_metadata_channels.json"""
        response = requests.post(
            f"{self.url}/setup/metadata_channels",
            json=self.metadata.model_dump(),
            headers={
                "Authorization": f"Bearer {self.token.id_token}", 
                "x-fake-application-name": self.client_info.application_name
                },
            timeout=10,
        )
        response.raise_for_status()
        print(f"Metadata каналы успешно загружены: {self.client_info.application_name}:{self.token.id_token}")

    def load_runtime_channels(self):
        """Загрузить runtime каналы из get_runtime_channels.json"""
        response = requests.post(
            f"{self.url}/setup/runtime_channels",
            json=self.runtime.model_dump(),
            headers={
                "Authorization": f"Bearer {self.token.id_token}", 
                "x-fake-application-name": self.client_info.application_name
            },
            timeout=10,
            )
        response.raise_for_status()
        print(f"Runtime каналы успешно загружены: {self.client_info.application_name}:{self.token.id_token}")


