from flask import abort
import pandas as pd

from src.server.core.item import ItemTable
from src.server.core.recipe import RecipeTable


class IngredientTable:
    """
    Singleton class for managing the 'ingredient' table.
    """

    _ingredients: pd.DataFrame = pd.DataFrame(
        columns=["INGREDIENT_ID", "ITEM_ID", "RECIPE_ID", "RATE"]
    )

    def __init__(self):
        """
        Initializes the singleton instance if it doesn't already exist.
        """
        if IngredientTable._ingredients is None:
            IngredientTable._ingredients = pd.DataFrame(
                columns=["INGREDIENT_ID", "ITEM_ID", "RECIPE_ID", "RATE"]
            )

    def get_many(self) -> list:
        """
        Returns the current ingredients DataFrame.
        """
        return IngredientTable._ingredients.to_dict(orient="records")

    def get_one(self, entry_id: int) -> dict:
        """
        Returns the ingredient with the specified INGREDIENT_ID.
        """
        ingredient_row = IngredientTable._ingredients[
            IngredientTable._ingredients["INGREDIENT_ID"] == entry_id
        ]
        if ingredient_row.empty:
            abort(404, description=f"Ingredient with id {entry_id} not found")
        return ingredient_row.to_dict(orient="records")[0]

    def add_one(self, content: dict) -> dict:
        """
        Adds a new ingredient to the table.
        """
        if (
            content["INGREDIENT_ID"]
            in IngredientTable._ingredients["INGREDIENT_ID"].values
        ):
            abort(
                409,
                description=f"INGREDIENT_ID {content['INGREDIENT_ID']} already exists",
            )
        # Verrify that the RECEIPE_ID AND ITEM_ID exist in the respective tables
        if not ItemTable().query({"ITEM_ID": content["ITEM_ID"]}):
            abort(
                409,
                description=f"ITEM_ID {content['ITEM_ID']} does not exist in the item table",
            )
        if not RecipeTable().query({"RECIPE_ID": content["RECIPE_ID"]}):
            abort(
                409,
                description=f"RECIPE_ID {content['RECIPE_ID']} does not exist in the recipe table",
            )
        IngredientTable._ingredients = pd.concat(
            [
                IngredientTable._ingredients,
                pd.DataFrame([content]).reindex(
                    columns=IngredientTable._ingredients.columns
                ),
            ],
            ignore_index=True,
        )
        return {"message": "Ingredient added successfully"}

    def add_many(self, content: list) -> dict:
        """
        Adds multiple new ingredients to the table.
        """
        for entry in content:
            self.add_one(entry)
        return {"message": "Ingredients added successfully"}

    def update_or_create(self, entry_id: int, content: dict) -> dict:
        """
        Updates the ingredient with the specified INGREDIENT_ID.
        """
        if entry_id != content["INGREDIENT_ID"]:
            if entry_id not in IngredientTable._ingredients["INGREDIENT_ID"].values:
                abort(404, description=f"Ingredient with id {entry_id} not found")
            if (
                content["INGREDIENT_ID"]
                in IngredientTable._ingredients["INGREDIENT_ID"].values
            ):
                abort(
                    409,
                    description=f"INGREDIENT_ID {content['INGREDIENT_ID']} already exists",
                )
            if not ItemTable().query({"ITEM_ID": content["ITEM_ID"]}):
                abort(
                    409,
                    description=f"ITEM_ID {content['ITEM_ID']} does not exist in the item table",
                )
            if not RecipeTable().query({"RECIPE_ID": content["RECIPE_ID"]}):
                abort(
                    409,
                    description=f"RECIPE_ID {content['RECIPE_ID']} does not exist in the recipe table",
                )
            self.add_one(content)
            self.delete(entry_id)
            return {"message": "Ingredient updated successfully"}
        if entry_id in IngredientTable._ingredients["INGREDIENT_ID"].values:
            if not ItemTable().query({"ITEM_ID": content["ITEM_ID"]}):
                abort(
                    409,
                    description=f"ITEM_ID {content['ITEM_ID']} does not exist in the item table",
                )
            if not RecipeTable().query({"RECIPE_ID": content["RECIPE_ID"]}):
                abort(
                    409,
                    description=f"RECIPE_ID {content['RECIPE_ID']} does not exist in the recipe table",
                )
            IngredientTable._ingredients.loc[
                IngredientTable._ingredients["INGREDIENT_ID"] == entry_id
            ] = (
                pd.DataFrame([content])
                .reindex(columns=IngredientTable._ingredients.columns)
                .values
            )
            return {"message": "Ingredient updated successfully"}
        return self.add_one(content)

    def delete(self, entry_id: int) -> dict:
        """
        Deletes the ingredient with the specified INGREDIENT_ID.
        """
        if entry_id not in IngredientTable._ingredients["INGREDIENT_ID"].values:
            abort(404, description=f"Ingredient with id {entry_id} not found")
        IngredientTable._ingredients = IngredientTable._ingredients[
            IngredientTable._ingredients["INGREDIENT_ID"] != entry_id
        ]
        return {"message": "Ingredient deleted successfully"}

    def query(self, query: dict) -> list:
        """
        Queries the ingredient table.
        """
        return IngredientTable._ingredients.query(
            " and ".join([f"{key} == {value}" for key, value in query.items()])
        ).to_dict(orient="records")
