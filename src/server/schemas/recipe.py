"""
This module contains the schema for recipe objects.
"""

from marshmallow import fields
from src.server.schemas.base import Base


class RecipeSchema(Base):
    """
    Schema for an recipe.
    """

    RECIPE_ID = fields.Int(required=True, description="The unique ID of the recipe")
    NAME = fields.Str(required=True, description="The name of the recipe")
    DESCRIPTION = fields.Str(
        required=False, description="The description of the recipe"
    )
