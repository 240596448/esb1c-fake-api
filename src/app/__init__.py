"""Пакет приложения"""
from app.storage import storage
from app.routes import bp
import app.loader as loader
import app.models as models

__all__ = ['storage', 'bp', 'loader', 'models']
