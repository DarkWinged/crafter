from typing import Final, Literal


from .wrapper_tag import WrapperTag


class Form(WrapperTag):
    """
    A form context that opens and closes a form tag.
    """

    TAG: Final[Literal["form"]] = "form"

    def __init__(
        self,
        method: Literal["GET", "POST"],
        action: str,
        *classes: str,
        identifier: str | None = None,
        context: str | None = None,
        novalidate: bool | None = None,
        accept_charset: str | None = None,
        style: dict[str, str] | None = None,
        enctype: (
            Literal[
                "application/x-www-form-urlencoded", "multipart/form-data", "text/plain"
            ]
            | None
        ) = None,
        autocomplete: bool | None = None,
        **data: str,
    ):

        self._tag = f"<{self.TAG} "
        self._add_attribute("method", method)
        self._add_attribute("action", action)
        if identifier:
            self._add_attribute("id", identifier)
            self._identifier = identifier
        if accept_charset:
            self._add_attribute("accept-charset", accept_charset)
        if autocomplete:
            self._add_attribute("autocomplete", "on")
        if enctype:
            self._add_attribute("enctype", enctype)
        if novalidate:
            self._add_attribute("novalidate")
        if classes:
            self._add_attribute("class", " ".join(classes))
        if style:
            self._add_attribute(
                "style", "; ".join(f"{k}: {v}" for k, v in style.items())
            )
        for key, value in data.items():
            self._add_attribute(f"data-{key}", value)
        self._tag += ">"
        super().__init__(context)
