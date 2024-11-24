"""
Module for the base classes and protocols.
"""

from typing import Dict, Protocol


class TableProtocol(Protocol):
    """
    Protocol for a table.
    """

    def add_many(self, content: Dict) -> Dict:
        """
        Protocol for adding multiple entries to the table.
        """

    def get_many(self) -> Dict:
        """
        Protocol for getting all entries from the table.
        """

    def get_one(self, entry_entry_id: int) -> Dict:
        """
        Porotocol for getting a single entry from the table.
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

    def query(self, query: str) -> Dict:
        """
        Protocol for querying the table.
        """
