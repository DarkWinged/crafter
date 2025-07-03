"""
This module initializes the blueprints and registers them with the Flask-Smorest API.
"""

from flask import Flask
from flask_restful import Api

from . import base, ingredient, item, product, recipe, static


def init(api: Api, app: Flask, base_url: str = ""):
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
    base_url = base_url.rstrip("/")
    # Register each blueprint with the API instance
    endpoints = [blueprint.init(base_url) for blueprint in blueprints]
    if base_url:
        base_blp = base.init(
            [endpoint for _, endpoint in endpoints], url_prefix=base_url
        )
    else:
        base_blp = base.init([endpoint for _, endpoint in endpoints])

    for backend, frontend in endpoints:
        api.register_blueprint(backend)
        base_blp.register_blueprint(frontend)
    app.register_blueprint(base_blp)
    app.register_blueprint(static.init())


__all__ = ["init"]
