# -*- coding: utf-8 -*-
"""
utilities/path_utils.py — minimal resource path manager for MyApp Template
"""

from __future__ import annotations
import os, sys
from pathlib import Path


def is_frozen() -> bool:
    """Return True if running from PyInstaller bundle."""
    return getattr(sys, "frozen", False)


def app_root() -> Path:
    """Return base directory of the app, inside bundle or source tree."""
    if is_frozen():
        # Example: C:/MyApp/dist/_internal
        exe_dir = Path(sys.executable).resolve().parent
        internal = exe_dir / "_internal"
        return internal if internal.exists() else exe_dir
    return Path(__file__).resolve().parent.parent


def base_path(*parts: str) -> str:
    """
    Build a path relative to the app root.
    Example: base_path('resources', 'icons', 'logo.png')
    """
    return str(app_root().joinpath(*parts))


def resource_path(*parts: str) -> str:
    """
    Return path to a bundled resource file (image, ui, icon, etc.)
    """
    return base_path('resources', *parts)


def writable_path(*parts: str, create: bool = False) -> str:
    """
    Same as base_path() but optionally create the directory.
    Used for logs, exports, or user data.
    """
    path = app_root().joinpath(*parts)
    if create:
        os.makedirs(path, exist_ok=True)
    return str(path)
