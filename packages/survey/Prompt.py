# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the terminal
from .Console import Console


class Prompt:
    """
    The base of every interactive prompt: a message, an optional console, and an {ask} contract
    """

    def __init__(self, *, message, help=None, console=None, **kwds):
        super().__init__(**kwds)
        # the question put to the user
        self.message = message
        # an optional one-line elaboration
        self.help = help
        # the terminal to talk to, defaulting to a fresh view of the standard streams
        self.console = console if console is not None else Console()

    def ask(self):
        """
        Put the question to the user and return their answer; overridden by each prompt
        """
        # the base class has no interaction of its own
        raise NotImplementedError(
            f"prompt '{type(self).__name__}' must implement 'ask'"
        )


# end of file
