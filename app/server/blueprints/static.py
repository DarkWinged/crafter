import importlib
from flask import send_file
from flask_smorest import Blueprint


def init():
    blp = Blueprint(
        "Static",
        "Static",
        description="Endpoint for serving static files.",
    )

    @blp.route("/favicon.ico")
    def favicon():
        icon = importlib.resources.files("app.server.static").joinpath("favicon.ico")
        return send_file(icon, mimetype="image/x-icon")

    @blp.route("/styles.css")
    def styles():
        styles = importlib.resources.files("app.server.static").joinpath("styles.css")
        return send_file(styles, mimetype="text/css")

    return blp
