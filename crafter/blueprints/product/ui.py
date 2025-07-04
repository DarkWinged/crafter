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


def edit_product_form(
    product_id: int,
    item_id: int,
    recipe_id: int,
    rate: int,
    action: str,
):
    form_identifier = f"edit_{product_id}"
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
            name="PRODUCT_ID",
            identifier=f"edit_id_{product_id}",
            value=product_id or "0",
            form=form_identifier,
            readonly=True,
        )
        with Label(id_form.identifier):
            ctx += "PRODUCT_ID:\t"
        ctx += id_form
        item_form = Input(
            "number",
            name="ITEM_ID",
            identifier=f"edit_item_{product_id}",
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
            identifier=f"edit_recipe_{product_id}",
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
            identifier=f"edit_rate_{product_id}",
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
            identifier=f"edit_submit_{product_id}",
            form=form_identifier,
        )
        ctx += submit_button


def delete_product_form(product_id: int, action: str):
    form_identifier = f"delete_{product_id}"
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
            name="PRODUCT_ID",
            value=product_id or "0",
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


def new_product_form(next_id: int, action: str):
    form_identifier = f"new_product_{next_id}"
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
            name="PRODUCT_ID",
            identifier=f"new_id_{next_id}",
            value=next_id or "0",
            form=form_identifier,
            readonly=True,
        )
        with Label(id_form.identifier):
            ctx += "PRODUCT_ID:\t"
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
    Initializes the UI for product management.
    """
    blp = Blueprint(
        "Products",
        __name__,
        description="UI for managing products.",
        url_prefix="/products",
    )

    @blp.route("/", methods=["GET"])
    def index():
        """
        Render the html UI for product management.
        """
        product_list = table.get_many()
        submission_endpoint = url_for("Base.Products.forward_form")
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
                    for endpoint in ["Items", "Recipes", "Ingredients"]:
                        with ListItem():
                            with Anchor(url_for(f"Base.{endpoint}.index")):
                                context += endpoint
                    with ListItem():
                        with Anchor(url_for("Base.api")):
                            context += "Documentation"
            with Body("body-main"):
                with Heading(style={"text-align": "center"}):
                    context += "Products"
                with Div(
                    style={
                        "background-color": "aliceblue",
                        "padding": "20px",
                        "border": "1px dashed orangered",
                        "width": "fit-content",
                        "margin": "0 auto",
                    },
                ):
                    for product in product_list:
                        product_id = product["PRODUCT_ID"]
                        recipe_id = product["RECIPE_ID"]
                        item_id = product["ITEM_ID"]
                        rate = product["RATE"]
                        with Div("form-container"):
                            edit_product_form(
                                product_id,
                                item_id,
                                recipe_id,
                                rate,
                                submission_endpoint,
                            )
                            delete_product_form(product_id, submission_endpoint)
                    with Div("form-container"):
                        new_product_form(
                            table.get_next_id(),
                            submission_endpoint,
                        )

        html_content = context.render(
            formatter=lambda x: BeautifulSoup(x, "html5lib").prettify()
        )
        return Response(html_content, mimetype="text/html")

    @blp.route("/", methods=["POST"])
    @blp.response(200, description="Forward the request and reload the recipes page.")
    def forward_form():
        try:
            method = request.form["forward_method"]
            data = request.form.to_dict()
            product_id = int(data["PRODUCT_ID"])

            if method == "PUT":
                table.update_or_create(
                    product_id,
                    {
                        "PRODUCT_ID": product_id,
                        "ITEM_ID": int(data["ITEM_ID"]),
                        "RECIPE_ID": int(data["RECIPE_ID"]),
                        "RATE": int(data["RATE"]),
                    },
                )
            elif method == "DELETE":
                table.delete(product_id)
        except Exception as e:  # pylint: disable=W0718
            logger.error(f"Error processing form: {e}", exc_info=True)
        return redirect(url_for("Base.Products.index"))

    return blp
