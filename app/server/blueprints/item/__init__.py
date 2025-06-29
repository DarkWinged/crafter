from flask_smorest import Blueprint

from ...core import ItemTable
from .api import init as init_api
from .ui import init as init_ui


def init(url_prefix: str) -> tuple[Blueprint, Blueprint]:
    """
    Initializes both the API and UI blueprints for items.
    """
    table = ItemTable()
    return init_api(url_prefix, table), init_ui(table)


__all__ = ["init"]
