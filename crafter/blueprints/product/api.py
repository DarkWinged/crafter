from flask_smorest import Blueprint

from ... import __version__
from ...core import ProductTable
from ...schemas import ProductSchema, ProductQuery


def init(url_prefix: str, table: ProductTable) -> Blueprint:
    """
    Registers the product blueprint with the given API instance.
    """
    blp = Blueprint(
        "Products",
        __name__,
        description="Endpoints for managing products.",
        url_prefix=f"{url_prefix}/api/v{__version__.split('.')[0]}/products",
    )

    @blp.route("/", methods=["GET"])
    @blp.response(200, ProductSchema(many=True))
    def get_all_products():
        """
        Retrieve all products.
        """
        return table.get_many()

    @blp.route("/", methods=["POST"])
    @blp.arguments(ProductSchema(many=True))
    @blp.response(200)
    def create_products(products):
        """
        Create new products.
        """
        return table.add_many(products)

    @blp.route("/<int:product_id>", methods=["GET"])
    @blp.response(200, ProductSchema)
    def get_product(product_id):
        """
        Retrieve a product by its ID.
        """
        return table.get_one(product_id)

    @blp.route("/<int:product_id>", methods=["PUT"])
    @blp.arguments(ProductSchema)
    @blp.response(200)
    def update_product(updated_product, product_id):
        """
        Update or create a product by its ID.
        """
        return table.update_or_create(product_id, updated_product)

    @blp.route("/<int:product_id>", methods=["DELETE"])
    @blp.response(200)
    def delete_product(product_id):
        """
        Delete a product by its ID.
        """
        return table.delete(product_id)

    @blp.route("/query", methods=["POST"])
    @blp.arguments(ProductQuery)
    @blp.response(200, ProductSchema(many=True))
    def query_products(query):
        """
        Query for products.
        """
        return table.query(query)

    return blp
