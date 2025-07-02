"""
Endpoints for the base blueprint aka "/"
"""

import logging
from bs4 import BeautifulSoup
from flask import Response, redirect, url_for
from flask_smorest import Blueprint


from ..views import (
    ListItem,
    Anchor,
    Aside,
    Body,
    Div,
    UnorderedList,
    Heading,
    HTMLRoot,
    Head,
    Title,
    Link,
)


from ...utils import API_MAJOR_VERSION


logger = logging.getLogger(__name__)


def init(endpoints, url_prefix: str | None = None):
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
        with HTMLRoot() as context:
            with Head():
                context += Link(
                    rel="stylesheet",
                    href=url_for("Static.styles"),
                )
                with Title():
                    context += "Craftsman"
            with Aside("aside-nav"):
                with UnorderedList():
                    for endpoint in endpoints:
                        with ListItem():
                            with Anchor(url_for(f"Base.{endpoint.name}.index")):
                                context += endpoint.name
                    with ListItem():
                        with Anchor(url_for("Base.api")):
                            context += "Documentation"
            with Body("body-main"):
                with Heading(style={"text-align": "center"}):
                    context += "Craftsman"
                with Div(style={"text-align": "center"}):
                    context += "Welcome to Craftsman! a web application for calculating recipe costs and production rates."

        links_html = context.render(
            formatter=lambda x: BeautifulSoup(x, "html5lib").prettify()
        )
        return Response(links_html, mimetype="text/html")

    @blp.route("/api")
    @blp.response(
        200,
        description="Redirects to the API documentation.",
    )
    def api():
        if url_prefix:
            return redirect(f"{url_prefix}/api/v{API_MAJOR_VERSION}/docs")
        return redirect(f"/api/v{API_MAJOR_VERSION}/docs")

    return blp
