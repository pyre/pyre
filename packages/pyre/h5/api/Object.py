# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Location import Location


# a basic h5 object
class Object(Location):
    """
    The base class for all publicly visible h5 objects
    """

    # type factories
    from .. import schema as _pyre_schema

    # metamethods
    def __init__(self, layout=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # record my type
        self._pyre_layout = layout
        # all done
        return

    # framework hooks
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am an object
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onObject
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(object=self, **kwds)


# end of file
