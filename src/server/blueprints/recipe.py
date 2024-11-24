"""
Blueprint for recipe routes
"""

from flask_smorest import Blueprint
from src.server.core.recipe import RecipeTable
from src.server.schemas.recipe import RecipeSchema

blp = Blueprint(
    "Recipes",
    __name__,
    description="Endpoints for managing recipes.",
    url_prefix="/recipes",
)
recipe_table = RecipeTable()


def init(api):
    """
    Registers the recipe blueprint with the given API instance.
    """
    api.register_blueprint(blp)
    return {"url": blp.url_prefix, "name": blp.name}


@blp.route("/", methods=["GET"])
@blp.response(200, RecipeSchema(many=True))
def get_all_recipes():
    """
    Retrieve all recipes.
    """
    return recipe_table.get_many()


@blp.route("/", methods=["POST"])
@blp.arguments(RecipeSchema(many=True))
@blp.response(200)
def create_recipes(recipes):
    """
    Create new recipes.
    """
    return recipe_table.add_many(recipes)


@blp.route("/<int:recipe_id>", methods=["GET"])
@blp.response(200, RecipeSchema)
def get_recipe(recipe_id):
    """
    Retrieve a recipe by its ID.
    """
    return recipe_table.get_one(recipe_id)


@blp.route("/<int:recipe_id>", methods=["PUT"])
@blp.arguments(RecipeSchema)
@blp.response(200)
def update_recipe(updated_recipe, recipe_id):
    """
    Update or create a recipe by its ID.
    """
    return recipe_table.update_or_create(recipe_id, updated_recipe)


@blp.route("/<int:recipe_id>", methods=["DELETE"])
@blp.response(200)
def delete_recipe(recipe_id):
    """
    Delete a recipe by its ID.
    """
    return recipe_table.delete(recipe_id)
