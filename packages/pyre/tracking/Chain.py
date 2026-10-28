# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# a locator that links a location to the one that caused it
class Chain:
    """
    A locator that ties together two others in order to express that something in {next}
    caused {this} to be recorded
    """

    # meta methods
    def __init__(self, this: object, next: object, **kwds) -> None:
        """
        Link {this} location to {next}, the location that caused it; {next} may be unknown
        """
        # chain up
        super().__init__(**kwds)
        # save the two locations
        self.this = this
        self.next = next
        # all done
        return

    def __str__(self) -> str:
        """
        Render the chain, starting with the most recent location
        """
        # if the cause is known
        if self.next is not None:
            # show the whole chain
            return f"{self.this}, {self.next}"
        # otherwise, there is only the location itself
        return str(self.this)

    # implementation details
    __slots__ = "this", "next"


# end of file
