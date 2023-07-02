# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal

# superclass
from .Object import Object


# a basic h5 object
class Datatype(Object):
    """
    A named data type
    """

    # metamethods
    def __str__(self):
        """
        Human readable representation
        """
        # easy enough
        return f"named datatype at '{self._pyre_location}'"

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a dataset
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onDatatype
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(dataset=self, **kwds)


# end of file
