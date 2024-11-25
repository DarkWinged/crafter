"""
Module to load environment variables
"""

from src.utils.file_managment import read

vc = read("vc.yaml")
env = read(".env.yaml")

API_VERSION = vc.get("API_VERSION", "0.0.0")
APP_VERSION = vc.get("APP_VERSION", "0.0.0")
ARCHIVE_PATH = env.get("ARCHIVE_PATH", "")
HOST = env.get("HOST", "0.0.0.0")
PORT = env.get("PORT", 5000)
