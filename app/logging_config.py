"""
Compatibility shim: re-export `setup_logging` from top-level `logging_config.py` so
`from app.logging_config import setup_logging` works.
"""
from logging_config import setup_logging  # type: ignore

__all__ = ["setup_logging"]
