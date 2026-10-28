# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# a locator for a command line argument
class Command:
    """
    A locator that records the position of a command line argument
    """

    # meta methods
    def __init__(self, arg: str, **kwds) -> None:
        """
        Record the command line argument {arg}
        """
        # chain up
        super().__init__(**kwds)
        # save the argument
        self.arg = arg
        # all done
        return

    def __str__(self) -> str:
        """
        Render the argument
        """
        # say where the value came from
        return f"from the command line argument {self.arg!r}"

    # implementation details
    __slots__ = ("arg",)


# end of file
