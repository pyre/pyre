# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# declaration
class Interactive:
    """
    A locator that records a value set interactively, by a person, through a user interface
    """

    # constant
    source = "set interactively in {}"

    # meta methods
    def __init__(self, interface):
        # save the name of the user interface
        self.interface = interface
        # all done
        return

    def __str__(self):
        # say where the value was set
        return self.source.format(self.interface)

    # implementation details
    __slots__ = ("interface",)


# end of file
