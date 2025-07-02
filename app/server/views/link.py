from typing import Final, Literal


from .literals import INPUT_TYPE, LANG_CODE, NUMBER, URL
from .tag import Tag


class Link(Tag):
    """
    Represents the HTML <link> element.
    """

    TAG: Final[Literal["link"]] = "link"

    def __init__(
        self,
        href: URL,
        rel: Literal[
            "stylesheet",
            "icon",
            "canonical",
            "dns-prefetch",
            "author",
            "help",
            "license",
            "prev",
            "next",
            "search",
            "alternate",
        ],
        kind: (
            Literal["text/css", "image/png", "image/jpeg", "application/json"] | None
        ) = None,
        identifier: str | None = None,
        media: str | None = None,
        sizes: str | None = None,
        hreflang: LANG_CODE | None = None,
        crossorigin: Literal["anonymous", "use-credentials"] | None = None,
    ):
        self._tag = f"<{self.TAG}"
        self._add_attribute("href", href)
        self._add_attribute("rel", rel)
        if kind:
            self._add_attribute("type", kind)
        if identifier:
            self._add_attribute("id", identifier)
        if media:
            self._add_attribute("media", media)
        if sizes:
            self._add_attribute("sizes", sizes)
        if hreflang:
            self._add_attribute("hreflang", hreflang)
        if crossorigin:
            self._add_attribute("crossorigin", crossorigin)
        self._tag += ">"
