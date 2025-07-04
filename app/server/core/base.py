"""
Module for the base classes and protocols.
"""

from typing import Dict, List, Protocol


class TableProtocol(Protocol):
    """
    Protocol for a table.
    """

    def add_many(self, content: Dict) -> Dict:
        """
        Protocol for adding multiple entries to the table.
        """

    def get_many(self) -> List:
        """
        Protocol for getting all entries from the table.
        """

    def get_one(self, entry_entry_id: int) -> Dict:
        """
        Protocol for getting a single entry from the table.
        """

    def get_next_id(self) -> int:
        """
        Protocol for getting the next available ID for a new entry.
        """

    def add_one(self, content: Dict) -> Dict:
        """
        Protocol for adding a single entry to the table.
        """

    def update_or_create(self, entry_entry_id: int, content: Dict) -> Dict:
        """
        Protocol for updating or creating an entry in the table.
        """

    def delete(self, entry_entry_id: int) -> Dict:
        """
        Protocol for deleting an entry from the table.
        """

    def query(self, query: dict) -> List:
        """
        Protocol for querying the table.
        """
