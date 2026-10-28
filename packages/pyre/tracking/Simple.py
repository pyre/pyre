# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# a locator that names its source and nothing else
class Simple:
    """
    A locator that records a simple named source with no further details
    """

    # meta methods
    def __init__(self, source: object, **kwds) -> None:
        """
        Record the {source}
        """
        # chain up
        super().__init__(**kwds)
        # save the source
        self.source = source
        # all done
        return

    def __str__(self) -> str:
        """
        Render my source
        """
        # the source says it all
        return str(self.source)

    # implementation details
    __slots__ = ("source",)


# end of file
