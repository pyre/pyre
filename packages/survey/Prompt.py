# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework, for the terminal the user is connected to
import pyre

# the theme registry
from . import Theme as themes


class Prompt:
    """
    The base of every interactive prompt: a message, the user's terminal, a theme, and an {ask}
    contract
    """

    def __init__(self, *, message, help=None, theme=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # the question put to the user
        self.message = message
        # an optional one-line elaboration
        self.help = help
        # the one terminal the user is connected to
        self.terminal = pyre.executive.terminal
        # the palette to paint with, defaulting to the package-wide fallback
        self.theme = theme if theme is not None else themes.default()

    def paint(self, text: str, color) -> str:
        """
        Style {text} with {color}, but only when the terminal can actually show it
        """
        # ask the terminal the user is connected to for the color's escape sequence
        code = self.terminal.render(color)
        # a colorless terminal, or an absent palette, yields no code; hand the text back plain
        if not code:
            return text
        # otherwise wrap the text so the styling stops where it ends
        return f"{code}{text}{self.terminal.reset()}"

    def ask(self):
        """
        Put the question to the user and return their answer; overridden by each prompt
        """
        # the base class has no interaction of its own
        raise NotImplementedError(
            f"prompt '{type(self).__name__}' must implement 'ask'"
        )


# end of file
