"""
Module for the core of the server.
"""

from logging import Logger
import os.path
from ...utils import read, write

from .product import ProductTable
from .base import TableProtocol
from .item import ItemTable
from .recipe import RecipeTable
from .ingredient import IngredientTable


tables: list[tuple[str, TableProtocol]] = [
    ("items", ItemTable),
    ("recipes", RecipeTable),
    ("ingredients", IngredientTable),
    ("products", ProductTable),
]

logger = Logger(__file__)


def init(path: str) -> None:
    """
    Initialize the db tables.
    """
    extension = "yaml"
    for name, table in tables:
        logger.info("Initializing %s", name)
        full_path = os.path.join(path, f"{name}.{extension}")
        try:
            content = read(full_path)
            table().add_many(content)
        except FileNotFoundError:
            logger.error("File not found: %s", full_path)

    def offload() -> None:
        """
        Offload the db tables.
        """
        for name, table in tables:
            logger.info("Offloading %s", name)
            full_path = os.path.join(path, f"{name}.{extension}")
            content = table().get_many()
            write(full_path, content)

    return offload


__all__ = [
    "init",
    "ItemTable",
    "RecipeTable",
    "IngredientTable",
    "ProductTable",
    "tables",
]
