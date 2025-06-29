"""
Blueprint for product routes.
"""

from flask_smorest import Blueprint

from ...core import ProductTable


def init(table: ProductTable) -> Blueprint:
    """
    Initializes the UI for product management.
    """
    blp = Blueprint(
        "Products",
        __name__,
        description="UI for managing products.",
        url_prefix="/products",
    )

    @blp.route("/", methods=["GET"])
    def index():
        """
        Render the html UI for product management.
        """
        html_content = "<html><body>todo</body></html>"

        return html_content

    return blp
