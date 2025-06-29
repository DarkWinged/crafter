from flask_smorest import Blueprint

from ...core import RecipeTable


def init(table: RecipeTable) -> Blueprint:
    """
    Initializes the UI for the recipe table.
    """
    blp = Blueprint(
        "Recipes",
        __name__,
        description="UI for managing recipes.",
        url_prefix="/recipes",
    )

    @blp.route("/", methods=["GET"])
    def index():
        """
        Render the html UI for recipe management.
        """
        html_content = "<html><body>todo</body></html>"
        return html_content

    return blp
