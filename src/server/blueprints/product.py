"""
Blueprint for product routes.
"""

from flask_smorest import Blueprint
from src.server.core.product import ProductTable
from src.server.schemas.product import ProductSchema, ProductQuerySchema

blp = Blueprint(
    "Products",
    __name__,
    description="Endpoints for managing products.",
    url_prefix="/products",
)
product_table = ProductTable()


def init(api):
    """
    Registers the product blueprint with the given API instance.
    """
    api.register_blueprint(blp)
    return {"url": blp.url_prefix, "name": blp.name}


@blp.route("/", methods=["GET"])
@blp.response(200, ProductSchema(many=True))
def get_all_products():
    """
    Retrieve all products.
    """
    return product_table.get_many()


@blp.route("/", methods=["POST"])
@blp.arguments(ProductSchema(many=True))
@blp.response(200)
def create_products(products):
    """
    Create new products.
    """
    return product_table.add_many(products)


@blp.route("/<int:product_id>", methods=["GET"])
@blp.response(200, ProductSchema)
def get_product(product_id):
    """
    Retrieve a product by its ID.
    """
    return product_table.get_one(product_id)


@blp.route("/<int:product_id>", methods=["PUT"])
@blp.arguments(ProductSchema)
@blp.response(200)
def update_product(updated_product, product_id):
    """
    Update or create a product by its ID.
    """
    return product_table.update_or_create(product_id, updated_product)


@blp.route("/<int:product_id>", methods=["DELETE"])
@blp.response(200)
def delete_product(product_id):
    """
    Delete a product by its ID.
    """
    return product_table.delete(product_id)


@blp.route("/query", methods=["POST"])
@blp.arguments(ProductQuerySchema)
@blp.response(200, ProductSchema(many=True))
def query_products(query):
    """
    Query for products.
    """
    return product_table.query(query)
