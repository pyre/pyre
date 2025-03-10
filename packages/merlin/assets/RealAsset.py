# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# superclass
from .Asset import Asset


# class declaration
class RealAsset(Asset):
    """
    Encapsulation of an asset with a physical presence on the filesystem
    """

    # meta methods
    def __init__(self, node=None, path=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # store my state
        self.node = node
        self.path = path
        # all done
        return


# end of file
