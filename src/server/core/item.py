"""
Module for managing the 'item' table.
"""

from flask import abort
import pandas as pd


class ItemTable:
    """
    Singleton class for managing the 'item' table.
    """

    _items: pd.DataFrame = pd.DataFrame(columns=["item_id", "name"])

    def __init__(self):
        """
        Initializes the singleton instance if it doesn't already exist.
        """
        if ItemTable._items is None:
            ItemTable._items = pd.DataFrame(columns=["item_id", "name"])

    def get_items(self) -> dict:
        """
        Returns the current items DataFrame.
        """
        return ItemTable._items.to_dict(orient="records")

    def get_item(self, item_id: int) -> dict:
        """
        Returns the item with the specified item_id.
        """
        item_row = ItemTable._items[ItemTable._items["item_id"] == item_id]
        if item_row.empty:
            abort(404, description=f"Item with id {item_id} not found")
        return item_row.to_dict(orient="records")[0]

    def add_item(self, new_item: dict) -> dict:
        """
        Adds a new item to the table.
        """
        if new_item["item_id"] in ItemTable._items["item_id"].values:
            abort(409, description=f"Item ID {new_item['item_id']} already exists")
        new_item_df = pd.DataFrame([new_item])
        ItemTable._items = pd.concat([ItemTable._items, new_item_df], ignore_index=True)
        return {"message": "Item added successfully"}

    def add_items(self, new_items: list) -> dict:
        """
        Adds multiple new items to the table.
        """
        for new_item in new_items:
            if new_item["item_id"] in ItemTable._items["item_id"].values:
                abort(409, description=f"Item ID {new_item['item_id']} already exists")
        new_items_df = pd.DataFrame(new_items)
        ItemTable._items = pd.concat(
            [ItemTable._items, new_items_df], ignore_index=True
        )
        return ItemTable._items.query("item_id in @new_items_df.item_id").to_dict(
            orient="records"
        )

    def update_or_create_item(self, item_id: int, updated_item: dict) -> dict:
        """
        Updates or creates an item with the specified item_id.
        """
        if item_id in ItemTable._items["item_id"].values:
            ItemTable._items.loc[ItemTable._items["item_id"] == item_id] = updated_item
            return {"message": "Item updated successfully"}
        new_item_df = pd.DataFrame([updated_item])
        ItemTable._items = pd.concat([ItemTable._items, new_item_df], ignore_index=True)
        return {"message": "Item created successfully"}

    def delete_item(self, item_id: int) -> dict:
        """
        Deletes the item with the specified item_id.
        """
        if item_id not in ItemTable._items["item_id"].values:
            abort(404, description=f"Item with id {item_id} not found")
        ItemTable._items = ItemTable._items[ItemTable._items["item_id"] != item_id]
        return {"message": "Item deleted successfully"}
