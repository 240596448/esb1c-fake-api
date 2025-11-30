import sys
from pathlib import Path
import json
from esb1c import Application

base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
client_file = Path(__file__).parent / "client.json"
if not client_file.exists():
    print(f"Файл {client_file} не найден")
    sys.exit(1)

try:
    client_data = json.loads(client_file.read_text(encoding="utf-8"))
except Exception as e:
    print(f"Ошибка загрузки данных из файла {client_file}: {e}")
    sys.exit(1)

client_id = client_data["client_id"]
client_secret = client_data["client_secret"]

application = Application(
    url=f"{base_url}/applications/fake",
    client_id=client_id,
    client_secret=client_secret,
)
