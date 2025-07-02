from typing import Final, Literal
from .wrapper_tag import WrapperTag


class CommonTag(WrapperTag):
    """
    Base class for HTML tags that only accept common attributes.
    """

    TAG: Final[Literal[str]] = ""

    def __init__(
        self,
        *classes: str,
        context: str | WrapperTag | None = None,
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


class Aside(CommonTag):
    """
    Represents the HTML <aside> element.
    """

    TAG: Final[Literal["aside"]] = "aside"


class Body(CommonTag):
    """
    Represents the HTML <body> element.
    """

    TAG: Final[Literal["body"]] = "body"


class Div(CommonTag):
    """
    Represents a HTML <div> element.
    """

    TAG: Final[Literal["div"]] = "div"


class Footer(CommonTag):
    """
    Represents the HTML <footer> element.
    """

    TAG: Final[Literal["footer"]] = "footer"


class OrderedList(CommonTag):
    """
    Represents the HTML <ol> element.
    """

    TAG: Final[Literal["ol"]] = "ol"


class UnorderedList(CommonTag):
    """
    Represents the HTML <ul> element.
    """

    TAG: Final[Literal["ul"]] = "ul"
