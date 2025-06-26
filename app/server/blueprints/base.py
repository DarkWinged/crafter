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
        url_prefix=url_prefix or "",
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
        links_html = "<html><body>"
        for endpoint in endpoints:
            if url_prefix:
                links_html += f'<a href="{url_prefix}{endpoint.url_prefix}">{endpoint.name}</a><br>'
            else:
                links_html += f'<a href="{endpoint.url_prefix}">{endpoint.name}</a><br>'
        if url_prefix:
            links_html += f'<a href="{url_prefix}/docs">Swagger API Documentation</a>'
        else:
            links_html += '<a href="/docs">Swagger API Documentation</a>'
        links_html += "</body></html>"
        return Response(links_html, mimetype="text/html")

    for endpoint in endpoints:
        blp.register_blueprint(endpoint)

    api.register_blueprint(blp)
