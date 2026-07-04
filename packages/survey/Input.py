# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the base prompt
from .Prompt import Prompt


class Input(Prompt):
    """
    Ask for a line of free text, offering a default that stands when the user just hits enter
    """

    def __init__(self, *, default=None, **kwds):
        super().__init__(**kwds)
        # the value to return when the reply is left blank
        self.default = default

    def ask(self) -> str:
        """
        Read a line, falling back to the default on an empty reply
        """
        # show the default in brackets when there is one to offer
        hint = f" [{self.default}]" if self.default is not None else ""
        # a cooked read gives the user their terminal's own line editing for free
        reply = input(f"{self.paint(self.message, self.theme.message)}{hint}: ").strip()
        # a non-empty reply wins; otherwise the default, or the empty string when there is none
        if reply:
            return reply
        return self.default if self.default is not None else ""


# end of file
