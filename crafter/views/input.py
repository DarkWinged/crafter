from typing import Final, Literal

from .literals import INPUT_TYPE, LANG_CODE, NUMBER, URL
from .tag import Tag


class Input(Tag):
    """
    An input tag that can be used to create various types of input fields.
    """

    TAG: Final[Literal["input"]] = "input"

    def __init__(
        self,
        kind: INPUT_TYPE,
        *classes: str,
        name: str | None = None,
        value: str | None = None,
        identifier: str | None = None,
        style: dict[str, str] | None = None,
        hidden: bool | None = None,
        title: str | None = None,
        tabindex: int | None = None,
        lang: LANG_CODE | None = None,
        checked: bool | None = None,
        placeholder: str | None = None,
        maxlength: int | None = None,
        required: bool | None = None,
        readonly: bool | None = None,
        disabled: bool | None = None,
        autofocus: bool | None = None,
        autocomplete: bool | None = None,
        form: str | None = None,
        formaction: URL | None = None,
        formtarget: (
            Literal["_blank", "_self", "_parent", "_top", "framename"] | None
        ) = None,
        formenctype: (
            Literal[
                "application/x-www-form-urlencoded", "multipart/form-data", "text/plain"
            ]
            | None
        ) = None,
        formmethod: Literal["GET", "POST"] | None = None,
        formnovalidate: bool | None = None,
        accept: str | None = None,
        min_value: str | NUMBER | None = None,
        max_value: str | NUMBER | None = None,
        step: int | float | None = None,
        pattern: str | None = None,
        size: int | float | None = None,
        src: URL | None = None,
        alt: str | None = None,
        width: int | None = None,
        height: int | None = None,
        datalist: str | None = None,
        dirname: str | None = None,
        **data: str,
    ):
        """
        Initializes the input tag with various attributes.
        """
        self._tag = f"<{self.TAG} "
        self._add_attribute("type", kind)
        if classes:
            self._add_attribute("class", " ".join(classes))
        if name:
            self._add_attribute("name", name)
        if value:
            self._add_attribute("value", value)
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
        if tabindex is not None and tabindex != "":
            self._add_attribute("tabindex", str(tabindex))
        if lang:
            self._add_attribute("lang", lang)
        if checked:
            self._add_attribute("checked")
        if placeholder:
            self._add_attribute("placeholder", placeholder)
        if maxlength is not None and maxlength != "":
            self._add_attribute("maxlength", str(maxlength))
        if required:
            self._add_attribute("required")
        if readonly:
            self._add_attribute("readonly")
        if disabled:
            self._add_attribute("disabled")
        if autofocus:
            self._add_attribute("autofocus")
        if autocomplete is not None:
            self._add_attribute("autocomplete", "on" if autocomplete else "off")
        if form:
            self._add_attribute("form", form)
        if formaction:
            self._add_attribute("formaction", formaction)
        if formtarget:
            self._add_attribute("formtarget", formtarget)
        if formenctype:
            self._add_attribute("formenctype", formenctype)
        if formmethod:
            self._add_attribute("formmethod", formmethod)
        if formnovalidate:
            self._add_attribute("formnovalidate")
        if accept:
            self._add_attribute("accept", accept)
        if min_value is not None and min_value != "":
            self._add_attribute("min", str(min_value))
        if max_value is not None and max_value != "":
            self._add_attribute("max", str(max_value))
        if step is not None and step != "":
            self._add_attribute("step", str(step))
        if pattern:
            self._add_attribute("pattern", pattern)
        if size is not None and size != "":
            self._add_attribute("size", str(size))
        if src:
            self._add_attribute("src", src)
        if alt:
            self._add_attribute("alt", alt)
        if width is not None and width != "":
            self._add_attribute("width", str(width))
        if height is not None and height != "":
            self._add_attribute("height", str(height))
        if datalist:
            self._add_attribute("list", datalist)
        if dirname:
            self._add_attribute("dirname", dirname)
        for k, v in data.items():
            self._add_attribute(f"data-{k}", v)
        self._tag += ">"
