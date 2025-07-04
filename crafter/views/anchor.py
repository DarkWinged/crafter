from typing import Final, Literal

from .literals import FILE_PATH, INDEX, LANG_CODE, RELATION_TYPE, URL
from .wrapper_tag import WrapperTag


class Anchor(WrapperTag):
    """
    Represents an HTML <a> (anchor) tag.
    """

    TAG: Final[Literal["a"]] = "a"

    def __init__(
        self,
        href: URL,
        *classes: str,
        context: str | None = None,
        identifier: str | None = None,
        style: dict[str, str] | None = None,
        hidden: bool | None = None,
        title: str | None = None,
        tabindex: INDEX | None = None,
        rel: RELATION_TYPE | None = None,
        target: Literal["_self", "_blank", "_parent", "_top"] | None = None,
        kind: str | None = None,
        lang: LANG_CODE | None = None,
        media: str | None = None,
        ping: list[URL] | None = None,
        download: FILE_PATH | None = None,
        **data: str,
    ):
        self._tag = f"<{self.TAG} "
        self._add_attribute("href", href)
        if classes:
            self._add_attribute("class", " ".join(classes))
        if identifier:
            self._add_attribute("id", identifier)
            self._identifier = identifier
        if style:
            self._add_attribute(
                "style", "; ".join(f"{k}: {v}" for k, v in style.items())
            )
        if hidden:
            self._add_attribute("hidden")
        if title:
            self._add_attribute("title", title)
        if tabindex is not None:
            self._add_attribute("tabindex", tabindex)
        if rel:
            self._add_attribute("rel", rel)
        if target:
            self._add_attribute("target", target)
        if kind:
            self._add_attribute("type", kind)
        if lang:
            self._add_attribute("lang", lang)
        if media:
            self._add_attribute("media", media)
        if ping:
            self._add_attribute("ping", " ".join(ping))
        if download:
            self._add_attribute("download", download)
        for key, value in data.items():
            self._add_attribute(f"data-{key}", value)
        self._tag += ">"
        super().__init__(context)
