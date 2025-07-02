from typing import Final, Literal
from .wrapper_tag import WrapperTag


class SimpleTag(WrapperTag):
    """
    Base class for HTML tags that do not require additional attributes.
    """

    TAG: Final[Literal[str]] = ""

    def __init__(self, context: str | WrapperTag | None = None):
        self._tag = f"<{self.TAG}>"
        super().__init__(context)


class Head(SimpleTag):
    """
    Represents the HTML <head> element.
    """

    TAG: Final[Literal["head"]] = "head"


class Title(SimpleTag):
    """
    Represents the HTML <title> element.
    """

    TAG: Final[Literal["title"]] = "title"
