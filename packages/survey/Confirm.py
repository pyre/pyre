# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the base prompt
from .Prompt import Prompt


class Confirm(Prompt):
    """
    Ask a yes/no question, returning a bool; the default stands when the user just hits enter
    """

    def __init__(self, *, default=True, **kwds):
        super().__init__(**kwds)
        # the answer to assume on an empty reply
        self.default = default

    def ask(self) -> bool:
        """
        Read a reply and interpret it as a yes or a no
        """
        # spell out which way a bare enter will go by capitalizing the default
        hint = "Y/n" if self.default else "y/N"
        # a cooked read is plenty for a single word
        reply = input(f"{self.paint(self.message, self.theme.message)} [{hint}]: ").strip().lower()
        # nothing typed means take the default
        if not reply:
            return self.default
        # otherwise anything affirmative is a yes, everything else a no
        return reply in ("y", "yes")


# end of file
