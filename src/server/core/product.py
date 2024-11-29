from flask import abort
import pandas as pd

from src.server.core.item import ItemTable
from src.server.core.recipe import RecipeTable


class ProductTable:
    """
    Singleton class for managing the 'product' table.
    """

    _products: pd.DataFrame = pd.DataFrame(
        columns=["PRODUCT_ID", "ITEM_ID", "RECIPE_ID", "RATE"]
    )

    def __init__(self):
        """
        Initializes the singleton instance if it doesn't already exist.
        """
        if ProductTable._products is None:
            ProductTable._products = pd.DataFrame(
                columns=["PRODUCT_ID", "ITEM_ID", "RECIPE_ID", "RATE"]
            )

    def get_many(self) -> list:
        """
        Returns the current products DataFrame.
        """
        return ProductTable._products.to_dict(orient="records")

    def add_many(self, content: list) -> dict:
        """
        Adds multiple new products to the table.
        """
        for entry in content:
            self.add_one(entry)
        return {"message": "Products added successfully"}

    def get_one(self, entry_id: int) -> dict:
        """
        Returns the product with the specified PRODUCT_ID.
        """
        product_row = ProductTable._products[
            ProductTable._products["PRODUCT_ID"] == entry_id
        ]
        if product_row.empty:
            abort(404, description=f"Product with id {entry_id} not found")
        return product_row.to_dict(orient="records")[0]

    def add_one(self, content: dict) -> dict:
        """
        Adds a new product to the table.
        """
        if content["PRODUCT_ID"] in ProductTable._products["PRODUCT_ID"].values:
            abort(
                409,
                description=f"PRODUCT_ID {content['PRODUCT_ID']} already exists",
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
        ProductTable._products = pd.concat(
            [
                ProductTable._products,
                pd.DataFrame([content]).reindex(columns=ProductTable._products.columns),
            ],
            ignore_index=True,
        )
        return {"message": "Product added successfully"}

    def update_or_create(self, entry_id: int, content: dict) -> dict:
        """
        Updates or creates a product with the specified PRODUCT_ID.
        """
        if entry_id != content["PRODUCT_ID"]:
            if entry_id not in ProductTable._products["PRODUCT_ID"].values:
                abort(404, description=f"Product with id {entry_id} not found")
            if content["PRODUCT_ID"] in ProductTable._products["PRODUCT_ID"].values:
                abort(
                    409,
                    description=f"PRODUCT_ID {content['PRODUCT_ID']} already exists",
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
            return {"message": "Product updated successfully"}
        if entry_id in ProductTable._products["PRODUCT_ID"].values:
            ProductTable._products.loc[
                ProductTable._products["PRODUCT_ID"] == entry_id
            ] = content
            return {"message": "Product updated successfully"}
        return self.add_one(content)

    def delete(self, entry_id: int) -> dict:
        """
        Deletes the product with the specified PRODUCT_ID.
        """
        if entry_id not in ProductTable._products["PRODUCT_ID"].values:
            abort(404, description=f"Product with id {entry_id} not found")
        ProductTable._products = ProductTable._products[
            ProductTable._products["PRODUCT_ID"] != entry_id
        ]
        return {"message": "Product deleted successfully"}

    def query(self, query: dict) -> list:
        """
        Queries the product table using the given query.
        """
        return ProductTable._products.query(
            " and ".join([f"{key} == {value}" for key, value in query.items()])
        ).to_dict(orient="records")
