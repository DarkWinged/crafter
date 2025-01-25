"""
Module for the core of the server.
"""
import os.path
from logging import Logger
from typing import List, Tuple

from src.server.core import item, recipe, ingredient, base, product
from src.utils.file_managment import read, write


tables: List[Tuple[str, base.TableProtocol]] = [
    ("items", item.ItemTable),
    ("recipes", recipe.RecipeTable),
    ("ingredients", ingredient.IngredientTable),
    ("products", product.ProductTable),
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
        print(full_path)
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
            print(full_path)
            content = table().get_many()
            write(full_path, content)

    return offload
