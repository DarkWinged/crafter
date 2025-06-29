"""
Blueprint for item routes
"""

import logging
from bs4 import BeautifulSoup
from flask import Response, redirect, request, url_for
from flask_smorest import Blueprint


from ...views.anchor import Anchor
from ...views.list_item import ListItem
from ...views.input import Input
from ...views.label import Label
from ...views.html_root import HTMLRoot
from ...views.heading import Heading
from ...views.form import Form
from ...views.generic_tags import Aside, Body, Div, UnorderedList
from ...core import ItemTable


logger = logging.getLogger(__name__)


aside_style = {
    "position": "fixed",
    "top": "0",
    "left": "0",
    "padding-right": "20px",
    "height": "100vh",
    "background-color": "#f8f9fa",
    "box-shadow": "2px 0 5px rgba(0,0,0,0.1)",
    "display": "flex",
    "gap": "10px",
}
body_style = {
    "margin-left": "200px",
    "padding": "20px",
}
form_div_style = {
    "display": "flex",
    "flex-direction": "row",
    "gap": "10px",
    "justify-content": "center",
}
form_style = {
    "gap": "10px",
    "display": "flex",
    "flex-direction": "row",
}


def edit_item_form(item_id: int, item_name: str, action: str) -> None:
    form_identifier = f"edit_{item_id}"
    with Form("POST", action, identifier=form_identifier, style=form_style) as ctx:
        ctx += Input(
            "hidden",
            name="forward_method",
            value="PUT",
            identifier=f"{form_identifier}_forward_method",
            form=form_identifier,
        )
        id_form = Input(
            "number",
            name="id",
            identifier=f"edit_id_{item_id}",
            value=item_id,
            form=form_identifier,
            readonly=True,
        )
        with Label(id_form.identifier):
            ctx += "ID:\t"
        ctx += id_form
        name_form = Input(
            "text",
            name="name",
            value=item_name,
            identifier=f"edit_name_{item_id}",
            form=form_identifier,
        )
        with Label(name_form.identifier):
            ctx += "NAME:\t"
        ctx += name_form
        ctx += Input(
            "submit",
            name="submit",
            identifier=f"{form_identifier}_submit",
            form=form_identifier,
            value="Update",
        )


def delete_item_form(item_id: int, action: str) -> None:
    form_identifier = f"delete_{item_id}"
    with Form("POST", action, identifier=form_identifier, style=form_style) as ctx:
        ctx += Input(
            "hidden",
            name="forward_method",
            value="DELETE",
            identifier=f"{form_identifier}_forward_method",
            form=form_identifier,
        )
        ctx += Input(
            "hidden",
            name="id",
            value=item_id,
            readonly=True,
            form=form_identifier,
        )
        ctx += Input(
            "submit",
            name="submit",
            identifier=f"{form_identifier}_submit",
            form=form_identifier,
            value="Delete",
        )


def new_item_form(next_item_id: int, action: str) -> None:
    form_identifier = f"new_{next_item_id}"
    with Form("POST", action, identifier=form_identifier, style=form_style) as ctx:
        ctx += Input(
            "hidden",
            name="forward_method",
            value="PUT",
            identifier=f"{form_identifier}_forward_method",
            form=form_identifier,
        )
        id_form = Input(
            "number",
            name="id",
            value=next_item_id,
            readonly=True,
            form=form_identifier,
            identifier="new_id",
        )
        with Label(id_form.identifier):
            ctx += "ID:\t"
        ctx += id_form
        name_form = Input(
            "text",
            name="name",
            style={"margin-right": "5px"},
            form=form_identifier,
            identifier="new_name",
        )
        with Label(name_form.identifier):
            ctx += "NAME:\t"
        ctx += name_form
        ctx += Input(
            "submit",
            name="submit",
            identifier=f"{form_identifier}_submit",
            form=form_identifier,
            value="Create",
        )


def init(table: ItemTable) -> Blueprint:
    """
    Initializes the UI blueprint for item management endpoints.
    """
    blp = Blueprint(
        "Items",
        __name__,
        description="UI endpoints for managing items.",
        url_prefix="/items",
    )

    @blp.route("/", methods=["GET"])
    @blp.doc(exclude=True)
    @blp.response(
        200,
        description="Rendered HTML with the list of items and intractable options to create, update, or delete items.",
    )
    def index():
        """
        Returns a rendered HTML page with the list of items and options to create, update, or delete items.
        """
        items_list = table.get_many()
        form_action = url_for("Base.Items.forward_form")
        with HTMLRoot() as context:
            with Aside(style=aside_style):
                with UnorderedList():
                    with ListItem():
                        with Anchor(url_for("Base.index")):
                            context += "Home"
                    for endpoint in ["Recipes", "Products", "Ingredients"]:
                        with ListItem():
                            with Anchor(url_for(f"Base.{endpoint}.index")):
                                context += endpoint
                    with ListItem():
                        with Anchor(url_for("Base.api")):
                            context += "Documentation"
            with Body(style=body_style):
                with Heading(style={"text-align": "center"}):
                    context += "Items"
                with Div(
                    style={
                        "background-color": "aliceblue",
                        "padding": "20px",
                        "border": "1px dashed orangered",
                        "width": "fit-content",
                        "margin": "0 auto",
                    },
                ):
                    for item in items_list:
                        item_id = item["ITEM_ID"]
                        item_name = item["NAME"]
                        with Div(style=form_div_style):
                            edit_item_form(
                                item_id,
                                item_name,
                                form_action,
                            )
                            delete_item_form(
                                item_id,
                                form_action,
                            )

                    with Div(
                        style=form_div_style,
                    ):
                        new_item_form(
                            table.get_next_id(),
                            form_action,
                        )

        html_content = context.render(
            formatter=lambda x: BeautifulSoup(x, "html5lib").prettify()
        )
        return Response(html_content, mimetype="text/html")

    @blp.route("/", methods=["POST"])
    @blp.doc(exclude=True)
    @blp.response(200, description="Forward the request and reload the items page.")
    def forward_form():
        """
        Modify an item by its ID.
        """
        try:
            method = request.form["forward_method"]
            data = request.form.to_dict()
            item_id = int(data["id"])

            if method == "PUT":
                item_data = {"ITEM_ID": item_id, "NAME": data["name"]}
                table.update_or_create(item_id, item_data)
            if method == "DELETE":
                table.delete(item_id)
        except Exception as e:  # pylint: disable=W0718
            logger.error(
                "Error modifying item with ID %s: %s",
                data.get("id", "unknown_id"),
                e,
                exc_info=True,
            )
        return redirect(url_for("Base.Items.index"))

    return blp
