"""
This module initializes the blueprints and registers them with the Flask-Smorest API.
"""

from flask_restful import Api
from . import base, item, recipe, ingredient, product


def init(api: Api):
    """
    Initialize and register blueprints with Flask-Smorest API.
    """
    # List of blueprints to register
    blueprints = [item, recipe, ingredient, product]
    endpoints = []

    # Register each blueprint with the API instance
    for blueprint in blueprints:
        endpoint = blueprint.init(api)
        endpoints.append(endpoint)
    base.init(api, endpoints)


__all__ = [
    "init",
    "base",
    "item",
    "recipe",
    "ingredient",
    "product",
]
