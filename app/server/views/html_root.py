from typing import Final, Literal

from .literals import LANG_CODE
from .wrapper_tag import WrapperTag


class HTMLRoot(WrapperTag):
    """
    Represents the root HTML element of a document.
    """

    TAG: Final[Literal["html"]] = "html"
    _tag: str

    def __init__(
        self,
        lang: LANG_CODE = "en",
        context: (
            str | None
        ) = None,  # HtmlRoot only uses context for identification, not for inheritance
        xmlns: str | None = None,
    ):
        self._tag = f"<!DOCTYPE html><{self.TAG} "
        self._add_attribute("lang", lang)
        if xmlns:
            self._add_attribute("xmlns", xmlns)
        self._tag += ">"
        super().__init__(context)
