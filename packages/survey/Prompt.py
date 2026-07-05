# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the terminal, the color helpers, and the theme registry
from .Console import Console
from . import chroma
from . import Theme as themes


class Prompt:
    """
    The base of every interactive prompt: a message, a console, a theme, and an {ask} contract
    """

    def __init__(self, *, message, help=None, console=None, theme=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # the question put to the user
        self.message = message
        # an optional one-line elaboration
        self.help = help
        # the terminal to talk to, defaulting to a fresh view of the standard streams
        self.console = console if console is not None else Console()
        # the palette to paint with, defaulting to the package-wide fallback
        self.theme = theme if theme is not None else themes.default()

    def paint(self, text: str, code: str) -> str:
        """
        Style {text} with {code}, but only when the terminal can actually show it
        """
        # defer the decision about whether color is allowed to {_colorful}
        return chroma.paint(text, code, enabled=self._colorful())

    def ask(self):
        """
        Put the question to the user and return their answer; overridden by each prompt
        """
        # the base class has no interaction of its own
        raise NotImplementedError(
            f"prompt '{type(self).__name__}' must implement 'ask'"
        )

    def _colorful(self) -> bool:
        """
        Whether this prompt may emit color: allowed globally and talking to a real terminal
        """
        # color is on unless suppressed, and only when both ends are a terminal
        return chroma.enabled() and self.console.interactive()


# end of file
