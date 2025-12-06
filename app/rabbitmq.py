"""Модуль для работы с RabbitMQ"""
import pika
from typing import Optional


class RabbitMQClient:
    """Клиент для работы с RabbitMQ"""
    
    def __init__(self, host: Optional[str] = None, port: Optional[int] = None, 
                 username: Optional[str] = None, password: Optional[str] = None,
                 virtual_host: str = '/'):
        """
        Инициализация клиента RabbitMQ
        """
        self.host = host
        self.port = int(port)
        self.username = username
        self.password = password
        self.virtual_host = virtual_host
        self._connection: Optional[pika.BlockingConnection] = None
        self._channel: Optional[pika.channel.Channel] = None
    
    def connect(self):
        """Установить соединение с RabbitMQ"""
        if self._connection and not self._connection.is_closed:
            return
        
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.virtual_host,
            credentials=credentials
        )
        
        try:
            self._connection = pika.BlockingConnection(parameters)
            self._channel = self._connection.channel()
            print(f"Подключение к RabbitMQ установлено: {self.host}:{self.port}")
        except (pika.exceptions.AMQPConnectionError, pika.exceptions.AMQPChannelError, 
                pika.exceptions.ProbableAuthenticationError, pika.exceptions.ProbableAccessDeniedError) as e:
            print(f"Ошибка подключения к RabbitMQ: {e}")
            raise
    
    def close(self):
        """Закрыть соединение с RabbitMQ"""
        if self._channel and not self._channel.is_closed:
            self._channel.close()
        if self._connection and not self._connection.is_closed:
            self._connection.close()
        print("Соединение с RabbitMQ закрыто")
    
    def create_queue(self, queue_name: str, durable: bool = True):
        """
        Создать очередь в RabbitMQ
        """
        try:
            self._channel.queue_declare(queue=queue_name, durable=durable)
            print(f"Очередь создана: {queue_name}")
        except (pika.exceptions.AMQPConnectionError, pika.exceptions.AMQPChannelError) as e:
            print(f"Ошибка создания очереди {queue_name}: {e}")
            raise ValueError(f"Ошибка создания очереди {queue_name}: {e}")

    def __enter__(self):
        """Контекстный менеджер: вход"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Контекстный менеджер: выход"""
        self.close()


def create_queues(runtime_channels: dict, host: str, port: int, token: str):
    """
    Создать очереди в RabbitMQ на основе runtime_channels
    """
    items = runtime_channels.get('items', [])
    if not items:
        raise ValueError(f"runtime_channels.items - список каналов пуст")
    queue_names = []
    for item in items:
        if isinstance(item, dict) and 'destination' in item:
            destination = item['destination']
            if destination:
                queue_names.append(destination)
    if not queue_names:
        raise ValueError(f"Не найдено ни одной очереди для создания")

    try:
        with RabbitMQClient(host=host, port=port, username=token, password=token) as client:
            for queue_name in queue_names:
                client.create_queue(queue_name, durable=True)
    except (pika.exceptions.AMQPConnectionError, pika.exceptions.AMQPChannelError) as e:
        raise ValueError(f"Ошибка при создании очередей: {e}")
