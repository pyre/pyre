# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from ..standard import Columns as standard


# declaration
class Columns(standard.Columns):
    """
    Type declarators in the sqlite dialect that are different from standard SQL
    """

    # text
    def _pyre_onString(self, schema, **kwds):
        """
        Build the type declarator of a column of text
        """
        # text of unbounded length
        if schema.maxlen is None:
            # has a type of its own
            return "TEXT"
        # the rest are declared as standard SQL declares them
        return super()._pyre_onString(schema=schema, **kwds)

    # arrays
    def _pyre_onArray(self, schema, **kwds):
        """
        Refuse a column of arrays, which sqlite has no type for
        """
        # complain
        raise self._refusal(contents="arrays", **kwds)


# end of file
