from __future__ import annotations

from collections.abc import Callable
from typing import Final, Literal

from .tag import Tag


class EarlyRenderError(Exception):
    """
    Raised when an attempt is made to render a non-root node.
    """


class RootCollisionError(Exception):
    """
    Raised when an attempt is made to create a HTML root tag in a context where another HTML root tag already exists.
    """


class RootInversionError(Exception):
    """
    Raised when an attempt is made to create a HTML root tag in a context where a context already has a root tag that is not a HTML root tag.
    """


class WrapperTag(Tag):
    """
    An abstract base class for HTML tags.
    """

    contexts: dict[str, WrapperTag] = {}
    active_contexts: list[str] = []

    TAG: Final[Literal[str]] = ""
    context: list[str]
    context_name: str

    def __init__(self, context: str | WrapperTag | None = None):
        """
        Initializes the tag with a context and a tag name.
        """

        if isinstance(context, WrapperTag):
            self.context = context.context
            self.context_name = context.context_name
        elif isinstance(context, str):
            if context in self.contexts:
                if self.TAG == "html":
                    if self.contexts[context].TAG == "html":
                        raise RootCollisionError(
                            f"Cannot create <{self.TAG}> in context '{context}' — root already exists: <{self.contexts[context].TAG}>"
                        )

                    if self.contexts[context].TAG != self.TAG:
                        raise RootInversionError(
                            f"Attempted overwrite of non-HTML root tag '{self.contexts[context].TAG}' in context '{context}' with HTML root"
                        )
                self.context = self.contexts[context].context
                self.context_name = context
            else:
                self.context = []
                self.contexts[context] = self
                self.context_name = context
        elif context is None:
            if self.active_contexts:
                active_context = self.active_contexts[-1]
                if self.TAG == "html":
                    if self.contexts[active_context].TAG == "html":
                        raise RootCollisionError(
                            f"Cannot create <{self.TAG}> in context '{context}' — root already exists: <{self.contexts[context].TAG}>"
                        )
                    if self.contexts[active_context].TAG != self.TAG:
                        raise RootInversionError(
                            f"Attempted overwrite of non-HTML root tag '{self.contexts[active_context].TAG}' in context '{active_context}' with HTML root"
                        )
                self.context = self.contexts[active_context].context
                self.context_name = active_context
            else:
                self.context = []
                base_context_name = f"{self.TAG}"
                attempts = 1
                context_name = f"{base_context_name}_{attempts}"
                while context_name in self.contexts:
                    attempts += 1
                    context_name = f"{base_context_name}_{attempts}"
                self.context_name = context_name
                self.contexts[self.context_name] = self

        if not hasattr(self, "_tag"):
            self._tag = f"<{self.TAG}>"

    def __enter__(self) -> WrapperTag:
        self.context.append(self._tag)
        if self.context_name in self.active_contexts:
            self.active_contexts.remove(self.context_name)
        self.active_contexts.append(self.context_name)
        return self

    def __iadd__(self, content: str | Tag) -> WrapperTag:
        if not isinstance(content, (str, Tag)):
            raise TypeError(
                f"Content must be a string or Tag, got {type(content).__name__} instead."
            )
        if isinstance(content, Tag):
            self.context.append(content.tag)
        else:
            self.context.append(content)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.context.append(f"</{self.TAG}>")
        context_root = self.contexts[self.context_name]
        if self is context_root:
            self.active_contexts.remove(self.context_name)
            del self.contexts[self.context_name]

    def __str__(self) -> str:
        return self.render()

    def __repr__(self):
        return f"<{self.__class__.__name__} context='{self.context_name}' tag='{self._tag}'>"

    def render(
        self, separator: str = "", formatter: Callable[[str], str] | None = None
    ) -> str:
        """
        Joins the content with a separator and returns the result.
        """
        if self.context_name in self.active_contexts:
            raise EarlyRenderError(
                (
                    f"Attempted join on non-root node [{self!r}]"
                    f" on context [{self.context_name}],"
                    f" actual root is [{self.contexts[self.context_name]!r}]"
                )
            )
        if formatter:
            return formatter(separator.join(self.context))
        return separator.join(self.context)
