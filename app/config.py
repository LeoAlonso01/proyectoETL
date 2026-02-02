"""
Compatibility shim: re-export `Settings` from top-level `config.py` so `from app.config import Settings` works.
"""
from config import Settings  # type: ignore

__all__ = ["Settings"]
