"""
This module contains the schema for product objects.
"""

from marshmallow import fields
from .base import Base


class ProductSchema(Base):
    """
    Schema for an product.
    """

    # Primary key
    PRODUCT_ID = fields.Int(
        required=True, metadata={"Description": "The unique ID of the product"}
    )
    # Foreign keys
    ITEM_ID = fields.Int(
        required=True,
        metadata={
            "Description": "The unique ID of the item that is produced by the recipe"
        },
    )
    RECIPE_ID = fields.Int(
        required=True,
        metadata={
            "Description": "The unique ID of the recipe that produces the product"
        },
    )
    # Data fields
    RATE = fields.Int(
        required=True,
        metadata={
            "Description": "The rate at which the product is produced in the recipe"
        },
    )


class ProductQuery(Base):
    """
    Schema for an product query.
    """

    PRODUCT_ID = fields.Int(
        required=False, metadata={"Description": "The unique ID of the product"}
    )
    ITEM_ID = fields.Int(
        required=False,
        metadata={
            "Description": "The unique ID of the item that is produced by the recipe"
        },
    )
    RECIPE_ID = fields.Int(
        required=False,
        metadata={
            "Description": "The unique ID of the recipe that produces the product"
        },
    )
    RATE = fields.Int(
        required=False,
        metadata={
            "Description": "The rate at which the product is produced in the recipe"
        },
    )
