from typing import Final, Literal
from .wrapper_tag import WrapperTag


class BaseTag(WrapperTag):
    """
    Base class for all HTML tags.
    """

    TAG: Final[Literal[str]] = ""

    def __init__(self, context: str | WrapperTag | None = None):
        self._tag = f"<{self.TAG}>"
        super().__init__(context)


class Head(BaseTag):
    """
    Represents the HTML <head> element.
    """

    TAG: Final[Literal["head"]] = "head"


class Title(BaseTag):
    """
    Represents the HTML <title> element.
    """

    TAG: Final[Literal["title"]] = "title"
