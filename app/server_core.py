"""
Server core module.
"""

import atexit
from flask import Flask
from flask_smorest import Api

from .server import blueprints, core
from .utils import API_VERSION, ARCHIVE_PATH, HOST, PORT


def main(debug=True):
    """
    Server entry point.
    """

    app = Flask(__name__)
    app.logger.setLevel("DEBUG")

    app.config["API_TITLE"] = "Crafter API"
    app.config["API_VERSION"] = f"v{API_VERSION}"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_JSON_PATH"] = "openapi.json"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.25.0/"
    )

    atexit.register(core.init(ARCHIVE_PATH))
    api = Api(app)
    blueprints.init(api)

    app.run(host=HOST, port=PORT, debug=debug)
