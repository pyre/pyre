# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


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

    def __del__(self):
        # get my id
        hid = self.pyre_id
        # if it's valid
        if hid is not None:
            # close it
            hid.close()
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

    def pyre_clone(self, id=None, **kwds):
        """
        Make as faithful a clone of mine as possible
        """
        # if the user didn't specify an {id}
        if id is None:
            # use mine
            id = self.pyre_id
        # invoke my constructor
        return super().pyre_clone(id=id, **kwds)


# end of file
