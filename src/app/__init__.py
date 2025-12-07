"""Пакет приложения"""
from app.main import app
from app.storage import storage
from app.routes import bp
import app.loader as loader

__all__ = ['app', 'storage', 'bp', 'loader']
