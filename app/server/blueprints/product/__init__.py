from flask_smorest import Blueprint

from ...core import ProductTable
from .api import init as init_api
from .ui import init as init_ui


def init(url_prefix: str) -> tuple[Blueprint, Blueprint]:
    """
    Initializes the product frontend and backend.
    """
    table = ProductTable()
    return init_api(url_prefix, table), init_ui(table)


__all__ = ["init"]
