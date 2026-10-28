# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# a locator for a value that came from the nameserver
class NameLookup:
    """
    A locator that records a nameserver {key}, rendered as the name it stands for when needed
    """

    # meta methods
    def __init__(self, description: str, key: object, **kwds) -> None:
        """
        Record the {key} of a nameserver entry, and a {description} of how it was used
        """
        # chain up
        super().__init__(**kwds)
        # save the key
        self.key = key
        # and the description
        self.description = description
        # all done
        return

    def __str__(self) -> str:
        """
        Render the description, followed by the name the key stands for
        """
        # get access to the framework managers; the nameserver is consulted only when rendering,
        # so the name reflects its current state
        from ..framework.Dashboard import Dashboard

        # put it together
        return f"{self.description} {Dashboard.pyre_nameserver[self.key]}"

    # implementation details
    __slots__ = "key", "description"


# end of file
