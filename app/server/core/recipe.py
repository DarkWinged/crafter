"""
Module for managing the 'item' table.
"""

from flask import abort
import pandas as pd


class RecipeTable:
    """
    Singleton class for managing the 'recipe' table.
    """

    _recipes: pd.DataFrame = pd.DataFrame(columns=["RECIPE_ID", "NAME", "DESCRIPTION"])

    def __init__(self):
        """
        Initializes the singleton instance if it doesn't already exist.
        """
        if RecipeTable._recipes is None:
            RecipeTable._recipes = pd.DataFrame(
                columns=["RECIPE_ID", "NAME", "DESCRIPTION"]
            )

    def get_many(self) -> dict:
        """
        Returns the current recipes DataFrame.
        """
        return RecipeTable._recipes.to_dict(orient="records")

    def get_one(self, entry_id: int) -> dict:
        """
        Returns the recipe with the specified RECIPE_ID.
        """
        recipe_row = RecipeTable._recipes[RecipeTable._recipes["RECIPE_ID"] == entry_id]
        if recipe_row.empty:
            abort(404, description=f"Recipe with id  {entry_id}  not found")
        return recipe_row.to_dict(orient="records")[0]

    def get_next_id(self) -> int:
        """
        Returns the next available RECIPE_ID for a new recipe.
        """
        if RecipeTable._recipes.empty:
            return 0
        return RecipeTable._recipes["RECIPE_ID"].max() + 1

    def add_one(self, content: dict) -> dict:
        """
        Adds a new recipe to the table.
        """
        if content["RECIPE_ID"] in RecipeTable._recipes["RECIPE_ID"].values:
            abort(409, description=f"RECIPE_ID {content['RECIPE_ID']} already exists")
        RecipeTable._recipes = pd.concat(
            [
                RecipeTable._recipes,
                pd.DataFrame([content])
                .reindex(columns=RecipeTable._recipes.columns)
                .fillna(""),
            ],
            ignore_index=True,
        )
        return {"message": "Recipe added successfully"}

    def add_many(self, content: list) -> dict:
        """
        Adds multiple new recipes to the table.
        """
        for entry in content:
            if entry["RECIPE_ID"] in RecipeTable._recipes["RECIPE_ID"].values:
                abort(
                    409,
                    DESCRIPTION=f"RECIPE_ID {entry['RECIPE_ID']} already exists",
                )
        RecipeTable._recipes = pd.concat(
            [
                RecipeTable._recipes,
                pd.DataFrame(content)
                .reindex(columns=RecipeTable._recipes.columns)
                .fillna(""),
            ],
            ignore_index=True,
        )
        return {"message": "Recipes added successfully"}

    def update_or_create(self, entry_id: int, content: dict) -> dict:
        """
        Updates or creates a recipe by its ID.
        """
        if entry_id != content["RECIPE_ID"]:
            if entry_id not in RecipeTable._recipes["RECIPE_ID"].values:
                abort(404, description=f"RECIPE_ID  {entry_id}  not found")
            if content["RECIPE_ID"] in RecipeTable._recipes["RECIPE_ID"].values:
                abort(
                    409,
                    DESCRIPTION=f"RECIPE_ID {content['RECIPE_ID']} already exists",
                )
            self.add_one(content)
            self.delete(entry_id)
            return {"message": "Recipe updated successfully"}
        if entry_id in RecipeTable._recipes["RECIPE_ID"].values:
            RecipeTable._recipes.loc[RecipeTable._recipes["RECIPE_ID"] == entry_id] = (
                pd.DataFrame([content])
                .reindex(columns=RecipeTable._recipes.columns)
                .fillna("")
                .values
            )
            return {"message": "Recipe updated successfully"}
        return self.add_one(content)

    def delete(self, entry_id: int) -> dict:
        """
        Deletes a recipe by its ID.
        """
        if entry_id not in RecipeTable._recipes["RECIPE_ID"].values:
            abort(404, description=f"RECIPE_ID  {entry_id}  not found")
        RecipeTable._recipes = RecipeTable._recipes[
            RecipeTable._recipes["RECIPE_ID"] != entry_id
        ]
        return {"message": "Recipe deleted successfully"}

    def query(self, query: dict) -> dict:
        """
        Queries the recipe table.
        """
        return RecipeTable._recipes.query(
            " and ".join([f"{key} == {value}" for key, value in query.items()])
        ).to_dict(orient="records")
