"""Jinja2 environment."""

from typing import Any

from jinja2 import Environment, StrictUndefined


class StrictEnvironment(Environment):
    """Create strict Jinja2 environment.

    Jinja2 environment will raise error on undefined variable in template-
    rendering context.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(undefined=StrictUndefined, **kwargs)


def create_env() -> StrictEnvironment:
    """Create a (default) jinja environment."""

    return StrictEnvironment(keep_trailing_newline=True)
