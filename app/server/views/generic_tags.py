from typing import Final, Literal
from .wrapper_tag import WrapperTag


class GenericTag(WrapperTag):
    TAG: Final[Literal[str]] = ""

    def __init__(
        self,
        *classes: str,
        context: str | None = None,
        identifier: str | None = None,
        style: dict[str, str] | None = None,
        **data: str,
    ):
        self._tag = f"<{self.TAG}"
        if identifier:
            self._add_attribute("id", identifier)
            self._identifier = identifier
        if style:
            self._add_attribute(
                "style", "; ".join(f"{k}: {v}" for k, v in style.items())
            )
        if classes:
            self._add_attribute("class", " ".join(classes))
        for key, value in data.items():
            self._add_attribute(f"data-{key}", value)
        self._tag += ">"
        super().__init__(context)


class Div(GenericTag):
    """
    Represents a HTML <div> element.
    """

    TAG: Final[Literal["div"]] = "div"


class Body(GenericTag):
    """
    Represents the HTML <body> element.
    """

    TAG: Final[Literal["body"]] = "body"


class Aside(GenericTag):
    """
    Represents the HTML <aside> element.
    """

    TAG: Final[Literal["aside"]] = "aside"


class UnorderedList(GenericTag):
    """
    Represents the HTML <ul> element.
    """

    TAG: Final[Literal["ul"]] = "ul"


class OrderedList(GenericTag):
    """
    Represents the HTML <ol> element.
    """

    TAG: Final[Literal["ol"]] = "ol"
