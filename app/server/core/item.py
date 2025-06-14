"""
Module for managing the 'item' table.
"""

from flask import abort
import pandas as pd


class ItemTable:
    """
    Singleton class for managing the 'item' table.
    """

    _items: pd.DataFrame = pd.DataFrame(columns=["ITEM_ID", "NAME"])

    def __init__(self):
        """
        Initializes the singleton instance if it doesn't already exist.
        """
        if ItemTable._items is None:
            ItemTable._items = pd.DataFrame(columns=["ITEM_ID", "NAME"])

    def get_many(self) -> list:
        """
        Returns the current items DataFrame.
        """
        return ItemTable._items.to_dict(orient="records")

    def get_one(self, entry_id: int) -> dict:
        """
        Returns the item with the specified ITEM_ID.
        """
        item_row = ItemTable._items[ItemTable._items["ITEM_ID"] == entry_id]
        if item_row.empty:
            abort(404, description=f"Item with id {entry_id} not found")
        return item_row.to_dict(orient="records")[0]

    def add_one(self, content: dict) -> dict:
        """
        Adds a new item to the table.
        """
        if content["ITEM_ID"] in ItemTable._items["ITEM_ID"].values:
            abort(409, description=f"ITEM_ID {content['ITEM_ID']} already exists")
        ItemTable._items = pd.concat(
            [
                ItemTable._items,
                pd.DataFrame([content]).reindex(columns=ItemTable._items.columns),
            ],
            ignore_index=True,
        )
        return {"message": "Item added successfully"}

    def add_many(self, content: list) -> dict:
        """
        Adds multiple new items to the table.
        """
        for entry in content:
            if entry["ITEM_ID"] in ItemTable._items["ITEM_ID"].values:
                abort(409, description=f"ITEM_ID {entry['ITEM_ID']} already exists")
        ItemTable._items = pd.concat(
            [
                ItemTable._items,
                pd.DataFrame(pd.DataFrame(content)).reindex(
                    columns=ItemTable._items.columns
                ),
            ],
            ignore_index=True,
        )
        return {"message": "Items added successfully"}

    def update_or_create(self, entry_id: int, content: dict) -> dict:
        """
        Updates or creates an item with the specified ITEM_ID.
        """
        if entry_id != content["ITEM_ID"]:
            if entry_id not in ItemTable._items["ITEM_ID"].values:
                abort(404, description=f"Item with id {entry_id} not found")
            if content["ITEM_ID"] in ItemTable._items["ITEM_ID"].values:
                abort(409, description=f"ITEM_ID {content['ITEM_ID']} already exists")
            self.add_one(content)
            self.delete(entry_id)
            return {"message": "Item updated successfully"}
        if entry_id in ItemTable._items["ITEM_ID"].values:
            ItemTable._items.loc[ItemTable._items["ITEM_ID"] == entry_id] = (
                pd.DataFrame([content]).reindex(columns=ItemTable._items.columns).values
            )
            return {"message": "Item updated successfully"}
        return self.add_one(content)

    def delete(self, entry_id: int) -> dict:
        """
        Deletes the item with the specified ITEM_ID.
        """
        if entry_id not in ItemTable._items["ITEM_ID"].values:
            abort(404, description=f"Item with id {entry_id} not found")
        ItemTable._items = ItemTable._items[ItemTable._items["ITEM_ID"] != entry_id]
        return {"message": "Item deleted successfully"}

    def query(self, query: dict) -> list:
        """
        Queries the item table.
        """
        return ItemTable._items.query(
            " and ".join([f"{key} == {value}" for key, value in query.items()])
        ).to_dict(orient="records")
