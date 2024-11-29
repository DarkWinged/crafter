"""
This module contains the schema for ingrdient objects.
"""

from marshmallow import fields
from src.server.schemas.base import Base


class IngredientSchema(Base):
    """
    Schema for an ingridient.
    """

    # Primary key
    INGREDIENT_ID = fields.Int(
        required=True, description="The unique ID of the ingridient"
    )
    # Foreign keys
    ITEM_ID = fields.Int(
        required=True, description="The unique ID of the item used as an ingridient"
    )
    RECIPE_ID = fields.Int(
        required=True,
        description="The unique ID of the recipe that uses the ingridient",
    )
    # Data fields
    RATE = fields.Int(
        required=True,
        description="The rate at which the ingridient is used in the recipe",
    )


class IngredientQuery(Base):
    """
    Schema for an ingridient query.
    """

    INGREDIENT_ID = fields.Int(
        required=False, description="The unique ID of the ingridient"
    )
    ITEM_ID = fields.Int(
        required=False, description="The unique ID of the item used as an ingridient"
    )
    RECIPE_ID = fields.Int(
        required=False,
        description="The unique ID of the recipe that uses the ingridient",
    )
    RATE = fields.Int(
        required=False,
        description="The rate at which the ingridient is used in the recipe",
    )
