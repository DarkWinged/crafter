"""
Module to load environment variables
"""

from os import getenv, path
from .file_management import read

env_path = getenv("ENV_PATH")
if env_path and path.exists(env_path):
    env = read(env_path)
    ARCHIVE_PATH = env.get("ARCHIVE_PATH", "")
    HOST = env.get("HOST", "0.0.0.0")
    PORT = env.get("PORT", 5000)
else:
    ARCHIVE_PATH = getenv("ARCHIVE_PATH", "")
    HOST = getenv("SERVER_HOST", "0.0.0.0")
    PORT = getenv("SERVER_PORT") or 5000
