from typing import Final, Literal
from .wrapper_tag import WrapperTag


class Heading(WrapperTag):
    """
    A heading context that opens and closes a heading tag.
    """

    TAG: Final[Literal["h"]] = "h"

    def __init__(
        self,
        *classes: str,
        context: str | WrapperTag | None = None,
        level: int = 1,
        identifier: str | None = None,
        style: dict[str, str] | None = None,
    ):
        if not (1 <= level <= 6):
            raise ValueError("Heading level must be between 1 and 6.")
        self.level = level
        self._tag = f"<{self.TAG}{level} "
        if identifier:
            self._add_attribute("id", identifier)
            self._identifier = identifier
        if style:
            self._add_attribute(
                "style", "; ".join(f"{k}: {v}" for k, v in style.items())
            )
        if classes:
            self._add_attribute("class", " ".join(classes))
        self._tag += ">"
        super().__init__(context)

    def __exit__(self, exc_type, exc_value, traceback):
        self.context.append(f"</{self.TAG}{self.level}>")
