from flask_smorest import Blueprint

from ...core import RecipeTable
from .api import init as init_api
from .ui import init as init_ui


def init(url_prefix: str) -> tuple[Blueprint, Blueprint]:
    """
    Initializes the recipe frontend and backend.
    """
    table = RecipeTable()
    return init_api(url_prefix, table), init_ui(table)


__all__ = ["init"]
