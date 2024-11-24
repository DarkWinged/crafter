"""
This module contains the schema for item objects.
"""

from marshmallow import fields
from src.server.schemas.base import Base


class ItemSchema(Base):
    """
    Schema for an item.
    """

    ITEM_ID = fields.Int(required=True, description="The unique ID of the item")
    NAME = fields.Str(required=True, description="The name of the item")
