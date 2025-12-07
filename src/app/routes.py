"""Роуты для фейкового API"""
import base64
from flask import Blueprint, request, jsonify
from .storage import storage
from .rabbitmq import create_queues

bp = Blueprint('api', __name__)
application_name_header = "x-fake-application-name"

def auth_basic(request):
    """Проверить Basic authentication"""
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Basic '):
        raise ValueError("Basic authentication required")
    try:
        encoded = auth_header.split(' ')[1]
        decoded = base64.b64decode(encoded).decode('utf-8')
        client_id, client_secret = decoded.split(':', 1)
    except (ValueError, IndexError):
        raise ValueError("Invalid Basic authentication format")

    return client_id, client_secret

def auth_bearer(request):
    """Проверить Bearer authentication"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise ValueError("Bearer authentication required")
    try:
        token = auth_header.split(' ')[1].strip()
    except (ValueError, IndexError):
        raise ValueError("Invalid Bearer token format")
    return token


@bp.route('/setup/token', methods=['POST'])
def setup_token():
    """Загрузить данные токена для приложения"""
    try:
        client_id, client_secret = auth_basic(request)
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    try:
        key = storage.set_token((client_id, client_secret), data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    return jsonify({
        "status": "ok", 
        "response": "setup token success",
        "key": key,
        "value": data,
        }), 200


@bp.route('/setup/metadata_channels', methods=['POST'])
def setup_metadata_channels():
    """Загрузить metadata каналы для приложения"""
    try:
        token = auth_bearer(request)
    except ValueError as e:
        return jsonify({"error": str(e)}), 403

    application_name = request.headers.get(application_name_header)
    if not application_name:
        return jsonify({"error": f"{application_name_header} header is required"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    try:
        key = storage.set_metadata_channels(application_name, token, data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "status": "ok", 
        "response": "setup metadata channels success",
        "key": key,
        "value": data,
        }), 200

@bp.route('/setup/runtime_channels', methods=['POST'])
def setup_runtime_channels():
    """Загрузить runtime каналы для приложения"""
    try:
        token = auth_bearer(request)
    except ValueError as e:
        return jsonify({"error": str(e)}), 403

    application_name = request.headers.get(application_name_header)
    if not application_name:
        return jsonify({"error": f"{application_name_header} header is required"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    try:
        key = storage.set_runtime_channels(application_name, token, data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    return jsonify({
        "status": "ok", 
        "response": "setup runtime channels success",
        "key": key,
        "value": data,
        }), 200


@bp.route('/auth/oidc/token', methods=['POST'])
def get_token():
    """Получить токен (имитация POST запроса библиотеки)"""
    try:
        client_id, client_secret = auth_basic(request)
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    
    print(f"POST /auth/oidc/token: client_id: {client_id}")

    try:
        token_data = storage.get_token((client_id, client_secret))
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    
    return jsonify(token_data), 200

@bp.route('/applications/<application_name>/sys/esb/metadata/channels', methods=['GET'])
def get_metadata_channels(application_name: str):
    """Получить runtime каналы"""

    print(f"GET metadata channels: application_name: {application_name}")

    try:
        token = auth_bearer(request)
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    
    try:
        metadata_channels = storage.get_metadata_channels(application_name, token)
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    
    return jsonify(metadata_channels), 200


@bp.route('/applications/<application_name>/sys/esb/runtime/channels', methods=['GET'])
def get_runtime_channels(application_name: str):
    """Получить runtime каналы"""

    print(f"GET runtime channels: application_name: {application_name}")

    try:
        token = auth_bearer(request)
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
  
    try:
        runtime_channels = storage.get_runtime_channels(application_name, token)
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    
    if runtime_channels:
        try:
            host = request.host.split(':')[0]
            port = runtime_channels.get('port', 5672)
            create_queues(runtime_channels, host, port, token)
        except Exception as e:
            print(f"Error creating queues from runtime channels: \n{e}")
    
    return jsonify(runtime_channels), 200


@bp.route('/', methods=['GET'])
def root():
    return jsonify("1C:ESB Fake API"), 200
