"""
This module contains the schema for item objects.
"""

from marshmallow import fields
from src.server.schemas.base import Base


class ItemSchema(Base):
    """
    Schema for an item.
    """

    item_id = fields.Int(required=True, description="The unique ID of the item")
    name = fields.Str(required=True, description="The name of the item")
