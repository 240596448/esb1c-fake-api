"""Роуты для фейкового API"""
from flask import Blueprint, request, jsonify
from storage import storage
import base64

bp = Blueprint('api', __name__)

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
    
    application_name = request.headers.get('application_name')
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    try:
        storage.set_token(application_name, (client_id, client_secret), data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    return jsonify({
        "status": "ok", 
        "response": "setup token success",
        "key": client_id,
        "value": data,
        }), 200


@bp.route('/setup/metadata_channels', methods=['POST'])
def setup_metadata_channels():
    """Загрузить metadata каналы для приложения"""
    try:
        token = auth_bearer(request)
    except ValueError as e:
        return jsonify({"error": str(e)}), 403

    application_name = request.headers.get('application_name')
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    try:
        storage.set_metadata_channels(application_name, token, data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "status": "ok", 
        "response": "setup metadata channels success",
        "key": token,
        "value": data,
        }), 200

@bp.route('/setup/runtime_channels', methods=['POST'])
def setup_runtime_channels():
    """Загрузить runtime каналы для приложения"""
    try:
        token = auth_bearer(request)
    except ValueError as e:
        return jsonify({"error": str(e)}), 403

    application_name = request.headers.get('application_name')
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    try:
        storage.set_runtime_channels(application_name, token, data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    return jsonify({
        "status": "ok", 
        "response": "setup runtime channels success",
        "key": token,
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
        token = storage.get_token((client_id, client_secret))
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    
    return jsonify({
        "id_token": token,
        "token_type" : "Bearer",
        "access_token" : "Not implemented"
        }), 200


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
    
    return jsonify(runtime_channels), 200


@bp.route('/', methods=['GET'])
def root():
    return jsonify("1C:ESB Fake API"), 200
