"""Скрипт для загрузки данных из JSON файлов"""

import sys
from pathlib import Path
from requests.exceptions import ConnectionError as RequestsConnectionError
from app.loader import MultiConfig, ApplicationLoader

if __name__ == "__main__":
    description = """
    Загрузка данных в сервис по адресу <url>

    Использование:
    python load_default_data.py [<url>] [<data_dir>]
    <url> - адрес сервиса, по умолчанию http://localhost:5000
    <data_dir> - директория с сырыми данными ответов сервиса, по умолчанию ./data/example-esb-answer

    Примеры:
    python load_default_data.py
    python load_default_data.py http://localhost:5000
    python load_default_data.py http://localhost:5000 ./data/example-esb-answer
    """
    if len(sys.argv) == 1:
        print(description)

    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    print(f"Загрузка данных в сервис по адресу {base_url}")

    arg_dir = sys.argv[2] if len(sys.argv) > 2 else "data/example-esb-answer"
    data_dir = Path(__file__).parent / arg_dir
    print(f"Загрузка данных в сервис по адресу {base_url} из директории {data_dir.absolute()}")

    config = MultiConfig(data_dir)
    loader = ApplicationLoader(config, base_url)
    try:
        loader.load_token()
        loader.load_metadata()
        loader.load_runtime_channels()
    except RequestsConnectionError as e:
        print(f"Ошибка соединения с сервисом {base_url}:\n{e}")
    except Exception as e:
        print(f"Ошибка загрузки данных:\n{e}")
