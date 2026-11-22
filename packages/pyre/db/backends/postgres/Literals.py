# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from ..standard import Literals as standard


# declaration
class Literals(standard.Literals):
    """
    Literals in the postgres dialect that are different from standard SQL
    """

    # public data
    emptyArray = "'{}'"  # the literal of an empty array, which takes the type of its column

    # strings of octets
    def _pyre_onBytes(self, schema, value, **kwds):
        """
        Render a string of octets
        """
        # as the hexadecimal digits postgres reads them from
        return f"'\\x{value.hex()}'"

    # times
    def _pyre_onTime(self, schema, value, **kwds):
        """
        Render a time of day
        """
        # postgres drops the offset of a plain time literal, so a time that has one
        if value.utcoffset() is not None:
            # must say so
            return f"TIME WITH TIME ZONE '{value.isoformat()}'"
        # the others are written as standard SQL writes them
        return super()._pyre_onTime(schema=schema, value=value, **kwds)

    def _pyre_onTimestamp(self, schema, value, **kwds):
        """
        Render a moment in time
        """
        # postgres drops the time zone of a plain timestamp literal, so a moment that has one
        if value.utcoffset() is not None:
            # must say so
            return f"TIMESTAMP WITH TIME ZONE '{value.isoformat(sep=' ')}'"
        # the others are written as standard SQL writes them
        return super()._pyre_onTimestamp(schema=schema, value=value, **kwds)

    # identifiers
    def _pyre_onUUID(self, schema, value, **kwds):
        """
        Render a universally unique identifier
        """
        # as its canonical text, quoted
        return self.mill.quote(text=str(value))

    # implementation details
    def _notANumber(self, **kwds):
        """
        Render a value that is not a number
        """
        # postgres has a literal for it
        return "'NaN'"

    def _infinity(self, positive, **kwds):
        """
        Render an infinity, {positive} or not
        """
        # postgres has a literal for each of them
        return "'Infinity'" if positive else "'-Infinity'"


# end of file
