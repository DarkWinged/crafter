"""
This module initializes the blueprints and registers them with the Flask-Smorest API.
"""

from flask import Flask
from flask_restful import Api
from . import base, item, recipe, ingredient, product, favicon


def init(api: Api, app: Flask, url_prefix: str = ""):
    """
    Initialize and register blueprints with Flask-Smorest API.
    """
    # List of blueprints to register
    blueprints = [
        item,
        recipe,
        product,
        ingredient,
    ]
    url_prefix = url_prefix.rstrip("/")
    # Register each blueprint with the API instance
    endpoints = [blueprint.init(url_prefix) for blueprint in blueprints]
    if url_prefix:
        base_blp = base.init(
            [endpoint for _, endpoint in endpoints], url_prefix=url_prefix
        )
    else:
        base_blp = base.init([endpoint for _, endpoint in endpoints])

    for backend, frontend in endpoints:
        api.register_blueprint(backend)
        base_blp.register_blueprint(frontend)
    app.register_blueprint(base_blp)
    favicon.init(app)


__all__ = ["init"]
