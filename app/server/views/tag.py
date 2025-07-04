import html
from abc import ABC
from typing import Final, Literal


class Tag(ABC):
    """
    An abstract base class for HTML tags.
    """

    TAG: Final[Literal[str]]
    _tag: str = ""
    _identifier: str | None = None

    def __init_subclass__(cls):
        if not hasattr(cls, "TAG"):
            raise AttributeError(
                f"Class {cls.__name__} must define a 'TAG' class attribute to specify the HTML tag name."
            )

    @property
    def tag(self) -> str:
        return self._tag

    @tag.setter
    def tag(self, _) -> None: ...

    @property
    def identifier(self) -> str | None:
        return self._identifier

    @identifier.setter
    def identifier(self, _) -> None: ...

    def _add_attribute(self, name: str, value: str | int | float | None = None) -> None:
        if not self._tag.endswith(" "):
            self._tag += " "
        if value is None:
            self._tag += f"{name}"
        else:
            self._tag += f'{name}="{html.escape(str(value))}"'

    def __str__(self) -> str:
        return self.tag
