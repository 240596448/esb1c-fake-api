# ESB 1C Fake API

Фейковый API сервер для имитации http-api 1С:ESB (Enterprise Service Bus).  
Предназначен для работы с RabbitMQ через сервисы интеграции (amqp 1.0).

## Описание

Сервис предоставляет REST API эндпоинты для:
- Аутентификации клиентов и получения токенов
- Настройки метаданных каналов (metadata channels)
- Настройки runtime каналов (runtime channels)
- Получения конфигурации каналов

Все данные хранятся в файловой системе в директории `app/storage` и сохраняются между перезапусками.

## Установка в Docker

### Предварительные требования

- Docker версии 20.10+
- Docker Compose версии 2.0+

### Запуск сервиса

1. Клонируйте репозиторий (если необходимо):
```bash
git clone <repository-url>
cd esb1c-fake-api
```

2. Соберите образ
```bash
docker build -t esb1c-fake-api .
```

3. Запустите контейнер
```bash
docker run -d 
    --name esb1c-fake-api 
    -p 9090:5000 
    -v ~/.fake/storage:/app/storage
    esb1c-fake-api
```
Сервис будет доступен по адресу `http://localhost:9090`

#### Примечание:
> Для сборки, старта и первичной загрузки данных - воспользуйтесь setup.sh

### DockerHub

Адрес на DockerHub: https://hub.docker.com/r/240596448/esb1c-fake-api
```bash
docker run -d 
    --name esb1c-fake-api 
    -p 9090:5000 
    -v ~/.fake/storage:/app/storage
    240596448/esb1c-fake-api
```
после установки требует обучения

## Принцип работы

В 1С указываем адрес контейнера как адрес приложения шины 1С в формате
```
http://localhost:9090/applications/<application_name>
```
где <application_name> - произвольное имя (ни на что не влияет)

1С получает предварительно загруженные данные с данного сервера (токен, каналы), формирует строку подключения amqp формата
`amqp://{id_token}:{id_token}@{host}:{port_amqp}applications/{application_name}`

Далее обращение производится к находящемуся по данному адресу RabbitMQ

## Аутентификация в RabbitMQ

Взять значение токена, загруженного в сервис для пользователя.  
> Смотри значение поля `id_token` из файла `get_token.json`. Например, `fake_secret_token_1C`

Создать пользователя в RabbitMQ
- логин: значение поля id_token
- пароль: значение поля id_token

Дать права на Exchanges и Vhost (требуются права на создание каналов).

_Альтернатива:_ использовать анонимную авторизацию (устанавливается в config RabbitMQ).

> Примечание:
Если требуется большое количество приложений, то чтобы не создавать много пользователей (разные токены), можно использовать одинаковый токен для разных приложений.

## Разрезы хранения данных

1. Загрузка/чтение токена: ключем хранения является `client_id`
2. Загрузка/чтение каналов: ключем хранения является `application_name`+`id_token`
    - `id_token` - берется из заголовка авторизации
    - при чтении/получении `application_name` берется из URL
    - при установке (при выполнении post-запроса в сервис) `application_name` требуется устанавливать в заголовок `x-fake-application-name`

## Загрузка/обучение сервиса

Перед использованием сервиса (настройкой каналов в 1С) необходимо загрузить данные из /data (токены, каналы и т.д.).
Это можно сделать с помощью скрипта `scripts/load_data.py`.

### Postman template collection

Коллекция загрузки(обучения) и проверки(чтения) результата [esb1c-fake.postman_collection.json](esb1c-fake.postman_collection.json)

### Подготовка данных

Убедитесь, что в директории `data/` присутствуют следующие файлы:
- `client.json` - содержит `application_name`, `client_id` и `client_secret`
- `get_token.json` - данные токена для загрузки
- `get_metadata.json` - метаданные каналов
- `get_runtime_channels.json` - runtime каналы

> [Более подробно](data/about_data.md) о содержимом файлов

### Загрузка данных

#### Вариант 1.
Загружает файлы `data/app-*.json` (все в одном):
```bash
python src/load_apps.py [url] [dir]
```
[Пример](src/data/app-1_single_data.json) формата и содержимого. 

Скрипт конвертирует файл в модели файлов ответов (вариант 2) и грузит их в сервис.

#### Вариант 2.
  Для загрузки исходных файлов-ответов из `data/example-esb-answer`:
```bash
python src/load_default_data.py [url] [dir]
```

Скрипт выполняет следующие действия:
1. Загружает данные токена через `/setup/token` (используя Basic auth из `client.json`)
2. Получает `id_token` из ответа
3. Загружает metadata каналы через `/setup/metadata_channels` (используя Bearer token)
4. Загружает runtime каналы через `/setup/runtime_channels` (используя Bearer token)

## API Эндпоинты

### POST /setup/token
Загрузить данные токена для приложения
- **Auth**: Basic (client_id:client_secret)
- **Body**: JSON с данными токена

### POST /setup/metadata_channels
Загрузить metadata каналы
- **Auth**: Bearer token
- **Body**: JSON с метаданными каналов

### POST /setup/runtime_channels
Загрузить runtime каналы
- **Auth**: Bearer token
- **Body**: JSON с runtime каналами

### POST /auth/oidc/token
Получить токен для приложения
- **Auth**: Basic (client_id:client_secret)
- **Returns**: JSON с `id_token`, `token_type`, `access_token`

### GET /applications/{application_name}/sys/esb/metadata/channels
Получить metadata каналы
- **Auth**: Bearer token
- **Returns**: JSON с метаданными каналов

### GET /applications/{application_name}/sys/esb/runtime/channels
Получить runtime каналы
- **Auth**: Bearer token
- **Returns**: JSON с runtime каналами

## Структура проекта

```
esb1c-fake-api/
├── src/
│   ├── app/
│   │   ├── __init__.py         # Инициализация Flask приложения
│   │   ├── loader.py           # Загрузка данных
│   │   ├── models.py           # Модели данных
│   │   ├── rabbitmq.py         # Работа с RabbitMQ
│   │   ├── routes.py           # Определение API эндпоинтов
│   │   └── storage.py          # Хранилище данных в памяти
│   ├── data/
│   │   ├── about_data.md                    # Описание структуры данных
│   │   ├── app-1 (single data).json         # Пример данных приложения
│   │   └── example-esb-answer/
│   │       ├── client.json                  # Учетные данные клиента
│   │       ├── get_token.json               # Данные токена (ответ запроса авторизации)
│   │       ├── get_metadata.json            # Metadata каналы (ответ запроса загрузки каналов)
│   │       └── get_runtime_channels.json    # Runtime каналы (ответ запроса подключения каналов)
│   ├── scripts/
│   │   └── test.py             # Тестовые скрипты
│   ├── storage/                # Постоянное хранилище загруженных данных сервиса (токены, каналы), монтируется в Docker
│   ├── load_apps.py            # Скрипт загрузки приложений
│   ├── load_default_data.py    # Скрипт загрузки данных по умолчанию
│   └── main.py                 # Точка входа приложения
├── Dockerfile
├── esb1c-fake.postman_collection.json  # Postman коллекция для тестирования
├── LICENSE
├── README.md
├── requirements.txt
└── setup.sh                    # Скрипт для сборки и запуска Docker, загрузки данных по умолчанию
```


## Хранение данных

Данные хранятся в файловой системе в директории `app/storage/`:
- Токены клиентов: `client_{client_id}.json`
- Metadata каналы: `metadata_{application_name}_{token}.json`
- Runtime каналы: `runtime_{application_name}_{token}.json`

