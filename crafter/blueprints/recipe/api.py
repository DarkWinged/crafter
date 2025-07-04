"""
Blueprint for recipe routes
"""

from flask_smorest import Blueprint

from ... import MAJOR_VERSION
from ...core import RecipeTable
from ...schemas import RecipeQuery, RecipeSchema


def init(url_prefix: str, table: RecipeTable) -> Blueprint:
    """
    Registers the recipe blueprint with the given API instance.
    """
    blp = Blueprint(
        "Recipes",
        __name__,
        description="Endpoints for managing recipes.",
        url_prefix=f"{url_prefix}/api/v{MAJOR_VERSION}/recipes",
    )

    @blp.route("/", methods=["GET"])
    @blp.response(200, RecipeSchema(many=True))
    def get_all_recipes():
        """
        Retrieve all recipes.
        """
        return table.get_many()

    @blp.route("/", methods=["POST"])
    @blp.arguments(RecipeSchema(many=True))
    @blp.response(200)
    def create_recipes(recipes):
        """
        Create new recipes.
        """
        return table.add_many(recipes)

    @blp.route("/<int:recipe_id>", methods=["GET"])
    @blp.response(200, RecipeSchema)
    def get_recipe(recipe_id):
        """
        Retrieve a recipe by its ID.
        """
        return table.get_one(recipe_id)

    @blp.route("/<int:recipe_id>", methods=["PUT"])
    @blp.arguments(RecipeSchema)
    @blp.response(200)
    def update_recipe(updated_recipe, recipe_id):
        """
        Update or create a recipe by its ID.
        """
        return table.update_or_create(recipe_id, updated_recipe)

    @blp.route("/<int:recipe_id>", methods=["DELETE"])
    @blp.response(200)
    def delete_recipe(recipe_id):
        """
        Delete a recipe by its ID.
        """
        return table.delete(recipe_id)

    @blp.route("/query", methods=["POST"])
    @blp.arguments(RecipeQuery)
    @blp.response(200, RecipeSchema(many=True))
    def query_recipes(query):
        """
        Query recipes by the given query.
        """
        return table.query(query)

    return blp
