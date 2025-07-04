"""
This module contains the schema for recipe objects.
"""

from marshmallow import fields
from .base import Base


class RecipeSchema(Base):
    """
    Schema for an recipe.
    """

    # Primary key
    RECIPE_ID = fields.Int(
        required=True, metadata={"Description": "The unique ID of the recipe"}
    )  # The unique ID of the recipe
    # Data fields
    NAME = fields.Str(
        required=True, metadata={"Description": "The name of the recipe"}
    )  # The name of the recipe
    DESCRIPTION = fields.Str(
        required=False, metadata={"Description": "The description of the recipe"}
    )  # The description of the recipe


class RecipeQuery(Base):
    """
    Schema for an recipe query.
    """

    RECIPE_ID = fields.Int(
        required=False, metadata={"Description": "The unique ID of the recipe"}
    )  # The unique ID of the recipe
    NAME = fields.Str(
        required=False, metadata={"Description": "The name of the recipe"}
    )  # The name of the recipe
    DESCRIPTION = fields.Str(
        required=False, metadata={"Description": "The description of the recipe"}
    )  # The description of the recipe
