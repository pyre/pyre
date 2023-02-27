# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# tiles
class Tile:
    """
    Encapsulation of a memory buffer, its shape, and its source
    """

    # metamethods
    def __init__(self, data, type, shape, origin, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my data source
        self.data = data
        # its type
        self.type = type
        # shape
        self.shape = shape
        # and origin
        self.origin = origin
        # all done
        return

    def __str__(self):
        # easy enough
        return f"{self.type}@{self.origin}+{self.shape}"


# end of file
