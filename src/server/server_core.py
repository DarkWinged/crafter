"""
Server core module.
"""

from flask import Flask
from flask_smorest import Api

from src.server import blueprints


def main():
    """
    Server entry point.
    """
    app = Flask(__name__)
    app.logger.setLevel("DEBUG")

    app.config["API_TITLE"] = "Crafter API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_JSON_PATH"] = "openapi.json"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.25.0/"
    )
    # app.config["LOG_FILE_PATH"] = LOG_FILE_PATH

    api = Api(app)

    blueprints.init(api)

    # Start the server
    app.run(host="0.0.0.0", port=5000, debug=True)
