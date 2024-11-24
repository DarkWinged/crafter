"""
Utility function to read a file and return its contents.
"""

import json
import os
import yaml


def read(path, encoding="utf-8"):
    """
    Read a file and return its contents.
    """
    if os.path.isdir(path):
        raise ValueError("Path is a directory")
    extension = path.split(".")[-1]
    if extension == "yaml":
        with open(path, "r", encoding=encoding) as file:
            return yaml.safe_load(file)
    elif extension == "json":
        with open(path, "r", encoding=encoding) as file:
            return json.load(file)
    elif extension == "txt":
        with open(path, "r", encoding=encoding) as file:
            return file.read()
    elif extension == "csv":
        with open(path, "r", encoding=encoding) as file:
            return file.read()
    elif extension == "tsv":
        with open(path, "r", encoding=encoding) as file:
            return file.read()
    else:
        raise ValueError("File type not supported")
