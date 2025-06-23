"""
Endpoints for the base blueprint aka "/"
"""

from flask import Response
from flask_smorest import Blueprint


def init(api, endpoints, url_prefix: str | None = None):
    """
    Initialize the base blueprint and populate dynamic links.
    """

    blp = Blueprint(
        "Base",
        __name__,
        description="General endpoints for server information.",
    )

    @blp.route("/")
    @blp.response(
        200,
        description="Rendered HTML with links to the endpoints and API documentation.",
    )
    def index():
        """
        Returns links to the other blueprints and to the API documentation.
        """
        # Build HTML links for the registered blueprints
        links_html = "<html><body>"
        for link in endpoints:
            links_html += f'<a href="{link["url"]}">{link["name"]}</a><br>'
        # Add Swagger API documentation link
        if url_prefix:
            links_html += (
                f'<a href="{url_prefix}/docs">' "Swagger API Documentation</a>"
            )
        else:
            links_html += '<a href="/docs">Swagger API Documentation</a>'
        links_html += "</body></html>"
        return Response(links_html, mimetype="text/html")

    api.register_blueprint(blp)
