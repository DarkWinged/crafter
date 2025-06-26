"""
This module initializes the blueprints and registers them with the Flask-Smorest API.
"""

from flask_restful import Api
from . import base, item, recipe, ingredient, product


def init(api: Api, url_prefix: str = ""):
    """
    Initialize and register blueprints with Flask-Smorest API.
    """
    # List of blueprints to register
    blueprints = [item, recipe, ingredient, product]
    url_prefix = url_prefix.rstrip("/")
    # Register each blueprint with the API instance
    endpoints = [blueprint.init() for blueprint in blueprints]
    if url_prefix:
        base_blp = base.init(endpoints, url_prefix=url_prefix)
    else:
        base_blp = base.init(endpoints)

    for endpoint in endpoints:
        base_blp.register_blueprint(endpoint)

    api.register_blueprint(base_blp)


__all__ = ["init"]
