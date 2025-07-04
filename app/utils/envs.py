"""
Module to load environment variables
"""

from os import getenv, path
from .file_management import read

vc_path = getenv("VC_PATH")
if vc_path and path.exists(vc_path):
    vc = read(vc_path)
    API_VERSION = vc.get("API_VERSION", "0.0.0")
    APP_VERSION = vc.get("APP_VERSION", "0.0.0")
else:
    API_VERSION = getenv("API_VERSION", "0.0.0")
    APP_VERSION = getenv("APP_VERSION", "0.0.0")

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

API_MAJOR_VERSION = API_VERSION.split(".")[0]
APP_MAJOR_VERSION = APP_VERSION.split(".")[0]
