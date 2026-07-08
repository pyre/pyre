# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


class Named:
    """
    Base class for objects that have names
    """

    # public data
    name = None

    # meta-methods
    def __init__(self, *, name=None, **kwds):
        super().__init__(**kwds)
        self.name = name
        return


# end of file
