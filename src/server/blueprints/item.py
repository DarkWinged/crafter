"""
Endpoints for the `/items` blueprint.
"""

from flask_smorest import Blueprint
from src.server.core.item import ItemTable
from src.server.schemas.item import ItemSchema

blp = Blueprint(
    "Items", __name__, description="Endpoints for managing items.", url_prefix="/items"
)

# Initialize the singleton instance
item_table = ItemTable()


def init(api):
    """
    Registers the item blueprint with the given API instance.
    """
    api.register_blueprint(blp)
    return {"url": blp.url_prefix, "name": blp.name}


@blp.route("/", methods=["GET"])
@blp.response(200, ItemSchema(many=True))
def get_all_items():
    """
    Retrieve all items.
    """
    return item_table.get_items()


@blp.route("/", methods=["POST"])
@blp.arguments(ItemSchema(many=True))
@blp.response(201, ItemSchema(many=True))
def create_items(items):
    """
    Create new items.
    """
    return item_table.add_items(items)


@blp.route("/<int:item_id>", methods=["GET"])
@blp.response(200, ItemSchema)
def get_item(item_id):
    """
    Retrieve an item by its ID.
    """
    return item_table.get_item(item_id)


@blp.route("/<int:item_id>", methods=["PUT"])
@blp.arguments(ItemSchema)
@blp.response(200, ItemSchema)
def update_item(updated_item, item_id):
    """
    Update or create an item by its ID.
    """
    return item_table.update_or_create_item(item_id, updated_item)


@blp.route("/<int:item_id>", methods=["DELETE"])
@blp.response(200)
def delete_item(item_id):
    """
    Delete an item by its ID.
    """
    return item_table.delete_item(item_id)
