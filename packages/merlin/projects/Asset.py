# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# class declaration
class Asset(merlin.component):
    """
    Encapsulation of an undifferentiated project asset

    This class is not meant to be instantiated directly; rather, it is the base of
    other, more useful classes
    """


    # required configurable state
    ignore = merlin.properties.bool(default=False)
    ignore.doc = "controls whether to ignore this asset"


    # meta methods
    def __init__(self, node, **kwds):
        # chain up
        super().__init__(**kwds)
        # store my node
        self.node = node
        # all done
        return


# end of file
