from flask_smorest import Blueprint

from ...core import IngredientTable


def init(table: IngredientTable) -> Blueprint:
    """
    Initializes the UI for ingredient management.
    """
    blp = Blueprint(
        "Ingredients",
        __name__,
        description="UI for managing ingredients.",
        url_prefix="/ingredients",
    )

    @blp.route("/", methods=["GET"])
    def index():
        """
        Render the html UI for ingredient management.
        """
        html_content = "<html><body>todo</body></html>"

        return html_content

    return blp
