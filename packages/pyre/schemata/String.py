# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import collections.abc  # for container identification

# superclass
from .Schema import Schema


# declaration
class String(Schema):
    """
    A type declarator for strings
    """

    # constants
    typename = "str"  # the name of my type
    complaint = "could not coerce {0.value!r} into a string"

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a string
        """
        # a map with entries is not text, even though it has one
        if isinstance(value, collections.abc.Mapping) and value:
            # so complain
            raise self.CastingError(value=value, description=self.complaint)
        # python can convert pretty much everything else into text; any other failures are
        # caused by issues in the {value} class, so let them through
        return str(value)

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a string
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onString
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

    # meta-methods
    def __init__(self, default=str(), **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file
