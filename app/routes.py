"""Роуты для фейкового API"""
from flask import Blueprint, request, jsonify
from app.storage import storage

bp = Blueprint('api', __name__)


@bp.route('/setup', methods=['POST'])
def setup_application():
    """Загрузить данные для приложения"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    application_name = data.get("application_name")
    if not application_name:
        return jsonify({"error": "application_name is required"}), 400
    
    token_data = data.get("token")
    metadata = data.get("metadata")
    runtime_channels = data.get("runtime_channels")
    
    if not all([token_data, metadata, runtime_channels]):
        return jsonify({"error": "token, metadata, and runtime_channels are required"}), 400
    
    storage.set_data(application_name, token_data, metadata, runtime_channels)
    
    return jsonify({"status": "ok", "application_name": application_name}), 200


@bp.route('/auth/oidc/token', methods=['POST'])
def get_token():
    """Получить токен (имитация POST запроса библиотеки)"""
    # Извлекаем application_name из заголовка или параметров
    application_name = request.headers.get('X-Application-Name') or request.args.get('application_name')
    
    if not application_name:
        return jsonify({"error": "application_name is required"}), 400
    
    token_data = storage.get_token(application_name)
    if token_data is None:
        return jsonify({"error": "Application not found"}), 404
    
    return jsonify(token_data), 200


@bp.route('/applications/<application_name>/sys/esb/metadata/channels', methods=['GET'])
def get_metadata(application_name: str):
    """Получить метаданные каналов"""
    metadata = storage.get_metadata(application_name)
    if metadata is None:
        return jsonify({"error": "Application not found"}), 404
    
    return jsonify(metadata), 200


@bp.route('/applications/<application_name>/sys/esb/runtime/channels', methods=['GET'])
def get_runtime_channels(application_name: str):
    """Получить runtime каналы"""
    runtime_channels = storage.get_runtime_channels(application_name)
    if runtime_channels is None:
        return jsonify({"error": "Application not found"}), 404
    
    return jsonify(runtime_channels), 200

