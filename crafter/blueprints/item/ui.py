import logging

from bs4 import BeautifulSoup
from flask import Response, redirect, request, url_for
from flask_smorest import Blueprint

from ...core import TableProtocol
from ...views import (
    Anchor,
    Aside,
    Body,
    Div,
    Form,
    Head,
    Heading,
    HTMLRoot,
    Input,
    Label,
    Link,
    ListItem,
    Title,
    UnorderedList,
)

logger = logging.getLogger(__name__)


def edit_item_form(item_id: int, item_name: str, action: str) -> None:
    form_identifier = f"edit_{item_id}"
    with Form("POST", action, identifier=form_identifier) as ctx:
        ctx += Input(
            "hidden",
            name="forward_method",
            value="PUT",
            identifier=f"{form_identifier}_forward_method",
            form=form_identifier,
        )
        id_form = Input(
            "number",
            name="ITEM_ID",
            identifier=f"edit_id_{item_id}",
            value=item_id or "0",
            form=form_identifier,
            readonly=True,
        )
        with Label(id_form.identifier):
            ctx += "ITEM_ID:\t"
        ctx += id_form
        name_form = Input(
            "text",
            name="NAME",
            value=item_name,
            identifier=f"edit_name_{item_id}",
            form=form_identifier,
            required=True,
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
    with Form("POST", action, identifier=form_identifier) as ctx:
        ctx += Input(
            "hidden",
            name="forward_method",
            value="DELETE",
            identifier=f"{form_identifier}_forward_method",
            form=form_identifier,
        )
        ctx += Input(
            "hidden",
            name="ITEM_ID",
            value=item_id or "0",
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
    with Form("POST", action, "form-container", identifier=form_identifier) as ctx:
        ctx += Input(
            "hidden",
            name="forward_method",
            value="PUT",
            identifier=f"{form_identifier}_forward_method",
            form=form_identifier,
        )
        id_form = Input(
            "number",
            name="ITEM_ID",
            value=next_item_id or "0",
            readonly=True,
            form=form_identifier,
            identifier="new_id",
        )
        with Label(id_form.identifier):
            ctx += "ITEM_ID:\t"
        ctx += id_form
        name_form = Input(
            "text",
            name="NAME",
            form=form_identifier,
            identifier="new_name",
            required=True,
        )
        with Label(name_form.identifier):
            ctx += "NAME:\t"
        ctx += name_form
        ctx += Input(
            "submit",
            name="submit",
            identifier=f"{form_identifier}_submit",
            style={
                "padding-right": "6px",
                "padding-left": "6px",
                "text-align": "center",
            },
            form=form_identifier,
            value="Create",
        )


def init(table: TableProtocol) -> Blueprint:
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
    @blp.response(
        200,
        description="Rendered HTML with the list of items and intractable options to create, update, or delete items.",
    )
    def index():
        """
        Returns a rendered HTML page with the list of items and options to create, update, or delete items.
        """
        items_list = table.get_many()
        submission_endpoint = url_for("Base.Items.forward_form")
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
            with Body("body-main"):
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
                        with Div("form-container"):
                            edit_item_form(
                                item_id,
                                item_name,
                                submission_endpoint,
                            )
                            delete_item_form(
                                item_id,
                                submission_endpoint,
                            )
                    with Div(
                        "form-container",
                    ):
                        new_item_form(
                            table.get_next_id(),
                            submission_endpoint,
                        )

        html_content = context.render(
            formatter=lambda x: BeautifulSoup(x, "html5lib").prettify()
        )
        return Response(html_content, mimetype="text/html")

    @blp.route("/", methods=["POST"])
    @blp.response(200, description="Forward the request and reload the items page.")
    def forward_form():
        """
        Modify an item by its ID.
        """
        try:
            method = request.form["forward_method"]
            data = request.form.to_dict()
            item_id = int(data["ITEM_ID"])

            if method == "PUT":
                item_data = {"ITEM_ID": item_id, "NAME": data["NAME"]}
                table.update_or_create(item_id, item_data)
            if method == "DELETE":
                table.delete(item_id)
        except Exception as e:  # pylint: disable=W0718
            logger.error(
                "Error modifying item with ID %s: %s",
                data.get("ITEM_ID", "unknown_id"),
                e,
                exc_info=True,
            )
        return redirect(url_for("Base.Items.index"))

    return blp
