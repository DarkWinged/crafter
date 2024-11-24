"""
Endpoints for the base blueprint aka "/"
"""

from flask import Response
from flask_smorest import Blueprint

blp = Blueprint(
    "Base",
    __name__,
    description="General endpoints for server information.",
)

links = []


def init(api, endpoints):
    """
    Initialize the base blueprint and populate dynamic links.
    """
    api.register_blueprint(blp)
    links.extend(endpoints)


@blp.route("/")
@blp.response(
    200, description="Rendered HTML with links to the endpoints and API documentation."
)
def index():
    """
    Returns links to the other blueprints and to the API documentation.
    """
    # Build HTML links for the registered blueprints
    links_html = "<html><body>"
    for link in links:
        links_html += f'<a href="{link["url"]}">{link["name"]}</a><br>'
    # Add Swagger API documentation link
    links_html += '<a href="/docs">Swagger API Documentation</a>'
    links_html += "</body></html>"
    return Response(links_html, mimetype="text/html")
