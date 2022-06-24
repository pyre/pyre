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


    # framework hooks
    def pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am an object
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority.pyre_onObject
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super().pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(object=self, **kwds)


# end of file
