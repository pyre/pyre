# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# a locator for a value a person set through a user interface
class Interactive:
    """
    A locator that records a value set interactively, by a person, through a user interface
    """

    # meta methods
    def __init__(self, interface: str, **kwds) -> None:
        """
        Record the name of the user {interface}
        """
        # chain up
        super().__init__(**kwds)
        # save the name of the user interface
        self.interface = interface
        # all done
        return

    def __str__(self) -> str:
        """
        Render the place where the value was set
        """
        # say where the value was set
        return f"set interactively in {self.interface}"

    # implementation details
    __slots__ = ("interface",)


# end of file
