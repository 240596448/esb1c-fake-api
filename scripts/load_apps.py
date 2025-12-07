"""Загрузка данных приложений в сервис"""

import sys
from pathlib import Path
from app.loader import SingleConfig, ApplicationLoader

def load_app(path: str, url: str):
    config = SingleConfig(path)
    loader = ApplicationLoader(config, url)
    loader.load_token()
    loader.load_metadata()
    loader.load_runtime_channels()

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    print(f"Загружаем данные в {base_url}")

    data_dir = Path(__file__).parent.parent / "data"
    app_files = data_dir.glob("app-*.json")

    for app_file in app_files:
        print(f"Загружаем данные из файла {app_file}")
        try:
            load_app(str(app_file), base_url)
        except Exception as e:
            print(f"Ошибка загрузки данных из файла {app_file}: {e}")
            continue
