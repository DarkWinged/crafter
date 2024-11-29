"""
Blueprint for ingredient routes
"""

from flask_smorest import Blueprint
from src.server.core.ingredient import IngredientTable
from src.server.schemas.ingredient import IngredientSchema, IngredientQuery


blp = Blueprint(
    "Ingredients",
    __name__,
    description="Endpoints for managing ingredients.",
    url_prefix="/ingredients",
)
ingredient_table = IngredientTable()


def init(api):
    """
    Registers the ingredient blueprint with the given API instance.
    """
    api.register_blueprint(blp)
    return {"url": blp.url_prefix, "name": blp.name}


@blp.route("/", methods=["GET"])
@blp.response(200, IngredientSchema(many=True))
def get_all_ingredients():
    """
    Retrieve all ingredients.
    """
    return ingredient_table.get_many()


@blp.route("/", methods=["POST"])
@blp.arguments(IngredientSchema(many=True))
@blp.response(200)
def create_ingredients(ingredients):
    """
    Create new ingredients.
    """
    return ingredient_table.add_many(ingredients)


@blp.route("/<int:ingredient_id>", methods=["GET"])
@blp.response(200, IngredientSchema)
def get_ingredient(ingredient_id):
    """
    Retrieve an ingredient by its ID.
    """
    return ingredient_table.get_one(ingredient_id)


@blp.route("/<int:ingredient_id>", methods=["PUT"])
@blp.arguments(IngredientSchema)
@blp.response(200)
def update_ingredient(updated_ingredient, ingredient_id):
    """
    Update or create an ingredient by its ID.
    """
    return ingredient_table.update_or_create(ingredient_id, updated_ingredient)


@blp.route("/query", methods=["POST"])
@blp.arguments(IngredientQuery)
@blp.response(200, IngredientSchema(many=True))
def query_ingredients(query):
    """
    Query for ingredients.
    """
    return ingredient_table.query(query)


@blp.route("/<int:ingredient_id>", methods=["DELETE"])
@blp.response(200)
def delete_ingredient(ingredient_id):
    """
    Delete an ingredient by its ID.
    """
    return ingredient_table.delete(ingredient_id)
