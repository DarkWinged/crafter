from flask_smorest import Blueprint

from ....utils import API_MAJOR_VERSION
from ...core import ItemTable
from ...schemas import ItemQuery, ItemSchema


def init(url_prefix: str, table: ItemTable) -> Blueprint:
    """
    Initializes the API blueprint for item management endpoints.
    """
    blp = Blueprint(
        "Items",
        __name__,
        description="Endpoints for managing items.",
        url_prefix=f"{url_prefix}/api/v{API_MAJOR_VERSION}/items",
    )

    @blp.route("/", methods=["GET"])
    @blp.response(200, ItemSchema(many=True))
    def get_all_items():
        """
        Retrieve all items.
        """
        return table.get_many()

    @blp.route("/", methods=["POST"])
    @blp.arguments(ItemSchema(many=True))
    @blp.response(200)
    def create_items(items):
        """
        Create new items.
        """
        return table.add_many(items)

    @blp.route("/<int:item_id>", methods=["GET"])
    @blp.response(200, ItemSchema)
    def get_item(item_id):
        """
        Retrieve an item by its ID.
        """
        return table.get_one(item_id)

    @blp.route("/<int:item_id>", methods=["PUT"])
    @blp.arguments(ItemSchema)
    @blp.response(200)
    def update_item(updated_item, item_id):
        """
        Update or create an item by its ID.
        """
        return table.update_or_create(item_id, updated_item)

    @blp.route("/<int:item_id>", methods=["DELETE"])
    @blp.response(200)
    def delete_item(item_id):
        """
        Delete an item by its ID.
        """
        return table.delete(item_id)

    @blp.route("/query", methods=["POST"])
    @blp.arguments(ItemQuery)
    @blp.response(200, ItemSchema(many=True))
    def query_items(query):
        """
        Query for items.
        """
        return table.query(query)

    return blp
