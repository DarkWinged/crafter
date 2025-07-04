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


def edit_ingredient_form(
    ingredient_id: int,
    item_id: int,
    recipe_id: int,
    rate: int,
    action: str,
):
    form_identifier = f"edit_{ingredient_id}"
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
            name="INGREDIENT_ID",
            identifier=f"edit_id_{ingredient_id}",
            value=ingredient_id or "0",
            form=form_identifier,
            readonly=True,
        )
        with Label(id_form.identifier):
            ctx += "INGREDIENT_ID:\t"
        ctx += id_form
        item_form = Input(
            "number",
            name="ITEM_ID",
            identifier=f"edit_item_{ingredient_id}",
            min_value="0",
            value=item_id or "0",
            form=form_identifier,
        )
        with Label(item_form.identifier):
            ctx += "ITEM_ID:\t"
        ctx += item_form
        recipe_form = Input(
            "number",
            name="RECIPE_ID",
            identifier=f"edit_recipe_{ingredient_id}",
            min_value="0",
            value=recipe_id or "0",
            form=form_identifier,
        )
        with Label(recipe_form.identifier):
            ctx += "RECIPE_ID:\t"
        ctx += recipe_form
        rate_form = Input(
            "number",
            name="RATE",
            identifier=f"edit_rate_{ingredient_id}",
            min_value="0",
            value=rate or "0",
            form=form_identifier,
        )
        with Label(rate_form.identifier):
            ctx += "RATE:\t"
        ctx += rate_form
        submit_button = Input(
            "submit",
            value="Update",
            identifier=f"edit_submit_{ingredient_id}",
            form=form_identifier,
        )
        ctx += submit_button


def delete_ingredient_form(ingredient_id: int, action: str):
    form_identifier = f"delete_{ingredient_id}"
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
            name="INGREDIENT_ID",
            value=ingredient_id or "0",
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


def new_ingredient_form(next_id: int, action: str):
    form_identifier = f"new_ingredient_{next_id}"
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
            name="INGREDIENT_ID",
            identifier=f"new_id_{next_id}",
            value=next_id or "0",
            form=form_identifier,
            readonly=True,
        )
        with Label(id_form.identifier):
            ctx += "INGREDIENT_ID:\t"
        ctx += id_form
        item_form = Input(
            "number",
            name="ITEM_ID",
            identifier=f"new_item_{next_id}",
            value="0",
            min_value="0",
            form=form_identifier,
        )
        with Label(item_form.identifier):
            ctx += "ITEM_ID:\t"
        ctx += item_form
        recipe_form = Input(
            "number",
            name="RECIPE_ID",
            identifier=f"new_recipe_{next_id}",
            value="0",
            min_value="0",
            form=form_identifier,
        )
        with Label(recipe_form.identifier):
            ctx += "RECIPE_ID:\t"
        ctx += recipe_form
        rate_form = Input(
            "number",
            name="RATE",
            identifier=f"new_rate_{next_id}",
            value="0",
            min_value="0",
            form=form_identifier,
        )
        with Label(rate_form.identifier):
            ctx += "RATE:\t"
        ctx += rate_form
        submit_button = Input(
            "submit",
            value="Create",
            identifier=f"new_submit_{next_id}",
            form=form_identifier,
        )
        ctx += submit_button


def init(table: TableProtocol) -> Blueprint:
    """
    Initializes the UI for ingredient management.
    """
    blp = Blueprint(
        "Ingredients",
        __name__,
        description="UI for managing ingredients.",
        url_prefix="/ingredients",
    )

    @blp.route("/", methods=["GET"])
    def index():
        """
        Render the html UI for ingredient management.
        """
        ingredient_list = table.get_many()
        submission_endpoint = url_for("Base.Ingredients.forward_form")
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
                    for endpoint in ["Items", "Recipes", "Products"]:
                        with ListItem():
                            with Anchor(url_for(f"Base.{endpoint}.index")):
                                context += endpoint
                    with ListItem():
                        with Anchor(url_for("Base.api")):
                            context += "Documentation"
            with Body("body-main"):
                with Heading(style={"text-align": "center"}):
                    context += "Ingredients"

                with Div(
                    style={
                        "background-color": "aliceblue",
                        "padding": "20px",
                        "border": "1px dashed orangered",
                        "width": "fit-content",
                        "margin": "0 auto",
                    },
                ):
                    for ingredient in ingredient_list:
                        ingredient_id = ingredient["INGREDIENT_ID"]
                        recipe_id = ingredient["RECIPE_ID"]
                        item_id = ingredient["ITEM_ID"]
                        rate = ingredient["RATE"]
                        with Div("form-container"):
                            edit_ingredient_form(
                                ingredient_id,
                                item_id,
                                recipe_id,
                                rate,
                                submission_endpoint,
                            )
                            delete_ingredient_form(ingredient_id, submission_endpoint)
                    with Div("form-container"):
                        next_id = 1
                        if ingredient_list:
                            next_id = (
                                max(
                                    ingredient["INGREDIENT_ID"]
                                    for ingredient in ingredient_list
                                )
                                + 1
                            )
                        new_ingredient_form(
                            next_id,
                            submission_endpoint,
                        )

        html_content = context.render(
            formatter=lambda x: BeautifulSoup(x, "html5lib").prettify()
        )
        return Response(html_content, mimetype="text/html")

    @blp.route("/", methods=["POST"])
    @blp.response(
        200, description="Forward the request and reload the ingredients page."
    )
    def forward_form():
        """
        Modify an ingredient by its ID.
        """
        try:
            method = request.form["forward_method"]
            data = request.form.to_dict()
            ingredient_id = int(data["INGREDIENT_ID"])

            if method == "PUT":
                ingredient_data = {
                    "INGREDIENT_ID": ingredient_id,
                    "ITEM_ID": int(data["ITEM_ID"]),
                    "RECIPE_ID": int(data["RECIPE_ID"]),
                    "RATE": int(data["RATE"]),
                }
                table.update_or_create(ingredient_id, ingredient_data)
            if method == "DELETE":
                table.delete(ingredient_id)
        except Exception as e:  # pylint: disable=W0718
            logger.error(
                "Error modifying ingredient with ID %s: %s",
                data.get("INGREDIENT_ID", "unknown_id"),
                e,
                exc_info=True,
            )
        return redirect(url_for("Base.Ingredients.index"))

    return blp
