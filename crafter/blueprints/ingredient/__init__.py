from flask_smorest import Blueprint

from ...core import IngredientTable
from .api import init as init_api
from .ui import init as init_ui


def init(url_prefix: str) -> tuple[Blueprint, Blueprint]:
    """Initializes the ingredient blueprint and its UI."""
    table = IngredientTable()
    return init_api(url_prefix, table), init_ui(table)
