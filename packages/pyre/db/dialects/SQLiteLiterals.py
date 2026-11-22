# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .StandardLiterals import StandardLiterals


# declaration
class SQLiteLiterals(StandardLiterals):
    """
    Literals in the sqlite dialect that are different from standard SQL
    """

    # dates and times
    def _pyre_onDate(self, schema, value, **kwds):
        """
        Render a date
        """
        # sqlite keeps dates as text
        return self.mill.quote(text=value.isoformat())

    def _pyre_onTime(self, schema, value, **kwds):
        """
        Render a time of day
        """
        # sqlite keeps times of day as text
        return self.mill.quote(text=value.isoformat())

    def _pyre_onTimestamp(self, schema, value, **kwds):
        """
        Render a moment in time
        """
        # sqlite keeps moments as text
        return self.mill.quote(text=value.isoformat(sep=" "))

    # arrays
    def _pyre_onArray(self, schema, table, column, **kwds):
        """
        Refuse an array, which sqlite has no type for
        """
        # complain
        raise self._refusal(table=table, column=column, contents="arrays")


# end of file
