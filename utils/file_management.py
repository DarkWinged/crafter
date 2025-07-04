"""
Utility function to read a file and return its contents.
"""

import json
import os
import pandas as pd
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


def pd_read(path, encoding="utf-8"):
    """
    read a file and return its contents as a pandas DataFrame
    """
    if os.path.isdir(path):
        raise ValueError("Path is a directory")
    extension = path.split(".")[-1]
    if extension == "yaml":
        with open(path, "r", encoding=encoding) as file:
            content = yaml.safe_load(file)
            return pd.DataFrame(content, columns=content[0].keys())
    elif extension == "json":
        with open(path, "r", encoding=encoding) as file:
            content = json.load(file)
            return pd.DataFrame(content, columns=content[0].keys())
    elif extension == "csv":
        return pd.read_csv(path)
    elif extension == "tsv":
        return pd.read_csv(path, sep="\t")
    else:
        raise ValueError("File type not supported")


def write(path, content, encoding="utf-8"):
    """
    Write to a file.
    """
    if os.path.isdir(path):
        raise ValueError("Path is a directory")
    extension = path.split(".")[-1]
    if extension == "yaml":
        with open(path, "w", encoding=encoding) as file:
            yaml.dump(content, file)
    elif extension == "json":
        with open(path, "w", encoding=encoding) as file:
            json.dump(content, file)
    elif extension == "txt":
        with open(path, "w", encoding=encoding) as file:
            file.write(content)
    elif extension == "csv":
        with open(path, "w", encoding=encoding) as file:
            file.write(content)
    elif extension == "tsv":
        with open(path, "w", encoding=encoding) as file:
            file.write(content)
    else:
        raise ValueError("File type not supported")


def pd_write(path, content, encoding="utf-8"):
    """
    Write a pandas DataFrame to a file.
    """
    if os.path.isdir(path):
        raise ValueError("Path is a directory")
    extension = path.split(".")[-1]
    if extension == "yaml":
        yaml.dump(content.to_dict(orient="records"), path, encoding=encoding)
    elif extension == "json":
        json.dump(content.to_dict(orient="records"), path, encoding=encoding)
    elif extension == "csv":
        content.to_csv(path, index=False)
    elif extension == "tsv":
        content.to_csv(path, sep="\t", index=False)
    else:
        raise ValueError("File type not supported")
