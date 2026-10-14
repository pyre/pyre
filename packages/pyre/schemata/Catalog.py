# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Mapping import Mapping


# declaration
class Catalog(Mapping):
    """
    The catalog type declarator
    """

    # constants
    typename = "catalog"  # the name of my type

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a catalog
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onCatalog
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)


# end of file
