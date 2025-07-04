from typing import Final, Literal

from .wrapper_tag import WrapperTag


class ListItem(WrapperTag):
    """
    Represents the HTML <li> element.
    """

    TAG: Final[Literal["li"]] = "li"

    def __init__(
        self,
        *classes: str,
        context: str | WrapperTag | None = None,
        identifier: str | None = None,
        style: dict[str, str] | None = None,
        hidden: bool | None = None,
        title: str | None = None,
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
        if hidden:
            self._add_attribute("hidden")
        if title:
            self._add_attribute("title", title)
        for key, value in data.items():
            self._add_attribute(f"data-{key}", value)
        self._tag += ">"
        super().__init__(context)
