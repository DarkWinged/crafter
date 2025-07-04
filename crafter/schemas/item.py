"""
This module contains the schema for item objects.
"""

from marshmallow import fields
from .base import Base


class ItemSchema(Base):
    """
    Schema for an item.
    """

    # Primary key
    ITEM_ID = fields.Int(
        required=True, metadata={"Description": "The unique ID of the item"}
    )
    # Data fields
    NAME = fields.Str(required=True, metadata={"Description": "The name of the item"})


class ItemQuery(Base):
    """
    Schema for an item query.
    """

    ITEM_ID = fields.Int(
        required=False, metadata={"Description": "The unique ID of the item"}
    )
    NAME = fields.Str(required=False, metadata={"Description": "The name of the item"})
