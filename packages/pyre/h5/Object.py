#-*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


# superclass
from .Location import Location


# a basic h5 object
class Object(Location):
    """
    The base class for all h5 objects
    """


    # metamethods
    def __init__(self, id=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # my handle
        self.pyre_id = id
        # all done
        return


# end of file
