from typing import Final, Literal

from .wrapper_tag import WrapperTag


class Label(WrapperTag):
    """
    Represents a label tag in HTML.
    """

    TAG: Final[Literal["label"]] = "label"

    def __init__(
        self,
        lfor: str,
        *classes: str,
        context: str | None = None,
        identifier: str | None = None,
        style: dict[str, str] | None = None,
        hidden: bool | None = None,
        title: str | None = None,
        **data: str,
    ):
        """
        Initializes the label tag with optional classes, identifier, style, and data attributes.
        """
        self._tag = f"<{self.TAG} "
        if identifier:
            self._add_attribute("id", identifier)
            self._identifier = identifier
        if lfor:
            self._add_attribute("for", lfor)
        if classes:
            self._add_attribute("class", " ".join(classes))
        if style:
            self._add_attribute(
                "style", "; ".join(f"{k}: {v}" for k, v in style.items())
            )
        if hidden:
            self._add_attribute("hidden")
        if title:
            self._add_attribute("title", title)
        for key, value in data.items():
            self._add_attribute(f"data-{key}", value)
        self._tag += ">"
        super().__init__(context)
