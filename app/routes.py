"""Роуты для фейкового API"""
from flask import Blueprint, request, jsonify
from storage import storage
import base64

bp = Blueprint('api', __name__)


@bp.route('/setup/token', methods=['POST'])
def setup_token():
    """Загрузить данные токена для приложения"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Basic '):
        return jsonify({"error": "Basic authentication required"}), 401
    
    try:
        encoded = auth_header.split(' ')[1]
        decoded = base64.b64decode(encoded).decode('utf-8')
        client_id, client_secret = decoded.split(':', 1)
    except (ValueError, IndexError):
        return jsonify({"error": "Invalid Basic authentication format"}), 401

    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    try:
        storage.set_token((client_id, client_secret), data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    return jsonify({
        "status": "ok", 
        "response": "setup token success",
        }), 200


@bp.route('/setup/runtime_channels', methods=['POST'])
def setup_runtime_channels():
    """Загрузить runtime каналы для приложения"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    application_name = data.get("application_name")
    if not application_name:
        return jsonify({"error": "application_name is required"}), 400
    
    storage.set_runtime_channels(application_name, data)
    
    return jsonify({"status": "ok", "application_name": application_name}), 200


@bp.route('/auth/oidc/token', methods=['GET'])
def get_token():
    """Получить токен (имитация POST запроса библиотеки)"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Basic '):
        return jsonify({"error": "Basic authentication required"}), 401
    
    try:
        encoded = auth_header.split(' ')[1]
        decoded = base64.b64decode(encoded).decode('utf-8')
        client_id, client_secret = decoded.split(':', 1)
    except (ValueError, IndexError):
        return jsonify({"error": "Invalid Basic authentication format"}), 401
    
    try:
        token = storage.get_token((client_id, client_secret))
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    
    return jsonify({
        "id_token": token,
        "token_type" : "Bearer",
        "access_token" : "Not implemented"
        }), 200


@bp.route('/applications/<application_name>/sys/esb/runtime/channels', methods=['GET'])
def get_runtime_channels(application_name: str):
    """Получить runtime каналы"""
    runtime_channels = storage.get_runtime_channels(application_name)
    if runtime_channels is None:
        return jsonify({"error": "Application not found"}), 404
    
    return jsonify(runtime_channels), 200

