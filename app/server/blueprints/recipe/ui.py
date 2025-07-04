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


def edit_recipe_form(
    recipe_id: int, recipe_name: str, recipe_description: str, action: str
) -> None:
    form_identifier = f"edit_{recipe_id}"
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
            name="RECIPE_ID",
            identifier=f"edit_id_{recipe_id}",
            value=recipe_id or "0",
            form=form_identifier,
            readonly=True,
        )
        with Label(id_form.identifier):
            ctx += "ID:\t"
        ctx += id_form
        name_form = Input(
            "text",
            name="NAME",
            value=recipe_name,
            identifier=f"edit_name_{recipe_id}",
            required=True,
            form=form_identifier,
        )
        with Label(name_form.identifier):
            ctx += "Name:\t"
        ctx += name_form
        description_form = Input(
            "text",
            name="DESCRIPTION",
            value=recipe_description,
            identifier=f"edit_description_{recipe_id}",
            required=True,
            form=form_identifier,
        )
        with Label(description_form.identifier):
            ctx += "DESCRIPTION:\t"
        ctx += description_form
        submit_button = Input(
            "submit",
            value="Update",
            identifier=f"edit_submit_{recipe_id}",
            form=form_identifier,
        )
        ctx += submit_button


def delete_recipe_form(recipe_id: int, action: str) -> None:
    form_identifier = f"delete_{recipe_id}"
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
            name="RECIPE_ID",
            value=recipe_id or "0",
            identifier=f"delete_id_{recipe_id}",
            form=form_identifier,
        )
        submit_button = Input(
            "submit",
            value="Delete",
            identifier=f"delete_submit_{recipe_id}",
            form=form_identifier,
        )
        ctx += submit_button


def new_recipe_form(next_id: int, action: str) -> None:
    form_identifier = f"new_recipe_{next_id}"
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
            name="RECIPE_ID",
            identifier=f"new_id_{next_id}",
            value=next_id or "0",
            form=form_identifier,
            readonly=True,
        )
        with Label(id_form.identifier):
            ctx += "RECIPE_ID:\t"
        ctx += id_form
        name_form = Input(
            "text",
            name="NAME",
            identifier=f"new_name_{next_id}",
            form=form_identifier,
        )
        with Label(name_form.identifier):
            ctx += "NAME:\t"
        ctx += name_form
        description_form = Input(
            "text",
            name="DESCRIPTION",
            identifier=f"new_description_{next_id}",
            required=True,
            form=form_identifier,
        )
        with Label(description_form.identifier):
            ctx += "Description:\t"
        ctx += description_form
        submit_button = Input(
            "submit",
            value="Create",
            identifier=f"new_submit_{next_id}",
            style={
                "padding-right": "6px",
                "padding-left": "6px",
                "text-align": "center",
            },
            required=True,
            form=form_identifier,
        )
        ctx += submit_button


def init(table: TableProtocol) -> Blueprint:
    """
    Initializes the UI for the recipe table.
    """
    blp = Blueprint(
        "Recipes",
        __name__,
        description="UI for managing recipes.",
        url_prefix="/recipes",
    )

    @blp.route("/", methods=["GET"])
    def index():
        """
        Render the html UI for recipe management.
        """
        recipe_list = table.get_many()
        submission_endpoint = url_for("Base.Recipes.forward_form")
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
                    for endpoint in ["Items", "Products", "Ingredients"]:
                        with ListItem():
                            with Anchor(url_for(f"Base.{endpoint}.index")):
                                context += endpoint
                    with ListItem():
                        with Anchor(url_for("Base.api")):
                            context += "Documentation"
            with Body("body-main"):
                with Heading(style={"text-align": "center"}):
                    context += "Recipes"
                with Div(
                    style={
                        "background-color": "aliceblue",
                        "padding": "20px",
                        "border": "1px dashed orangered",
                        "width": "fit-content",
                        "margin": "0 auto",
                    },
                ):
                    for recipe in recipe_list:
                        recipe_id = recipe["RECIPE_ID"]
                        recipe_name = recipe["NAME"]
                        recipe_description = recipe["DESCRIPTION"]
                        with Div("form-container"):
                            edit_recipe_form(
                                recipe_id,
                                recipe_name,
                                recipe_description,
                                submission_endpoint,
                            )
                            delete_recipe_form(recipe_id, submission_endpoint)
                    with Div("form-container"):
                        new_recipe_form(
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
            recipe_id = int(data["RECIPE_ID"])
            if method == "PUT":
                table.update_or_create(
                    recipe_id,
                    {
                        "RECIPE_ID": recipe_id,
                        "NAME": data["NAME"],
                        "DESCRIPTION": data["DESCRIPTION"],
                    },
                )
            elif method == "DELETE":
                table.delete(recipe_id)
        except Exception as e:  # pylint: disable=W0718
            logger.error(f"Error processing form: {e}", exc_info=True)
        return redirect(url_for("Base.Recipes.index"))

    return blp
