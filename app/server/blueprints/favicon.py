import importlib
from flask import send_file
from flask_smorest import Blueprint
from flask_restful import Api


def init(api: Api):
    favicon_blp = Blueprint(
        "Favicon",
        "Favicon",
        description="Endpoint for serving the favicon.",
    )

    @favicon_blp.route("/favicon.ico")
    def favicon():
        icon = importlib.resources.files("app.server.static").joinpath("favicon.ico")
        return send_file(icon, mimetype="image/x-icon")

    api.register_blueprint(favicon_blp)
