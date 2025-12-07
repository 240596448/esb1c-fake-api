"""Скрипт для загрузки данных из JSON файлов"""

import sys
from pathlib import Path
from app.loader import MultiConfig, ApplicationLoader

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    arg_dir = sys.argv[2] if len(sys.argv) > 2 else "data/example-esb-answer"
    data_dir = Path(__file__).parent / arg_dir
    print(f"Загрузка данных в сервис по адресу {base_url} и директории {data_dir.absolute()}")

    config = MultiConfig(data_dir)
    loader = ApplicationLoader(config, base_url)
    loader.load_token()
    loader.load_metadata()
    loader.load_runtime_channels()
