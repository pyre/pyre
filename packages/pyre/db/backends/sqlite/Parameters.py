# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from ..standard import Parameters as standard


# declaration
class Parameters(standard.Parameters):
    """
    The parameters of statements in the sqlite dialect, where they differ from standard SQL
    """

    # the forms the bindings take, by the type of the column; they are the forms the literals of
    # sqlite have, since the module that binds the values takes only numbers, text and octets
    def _pyre_onBoolean(self, schema, value, **kwds):
        """
        Keep a truth value
        """
        # as the integer sqlite keeps for it
        return int(value)

    def _pyre_onDecimal(self, schema, value, **kwds):
        """
        Keep a fixed point number
        """
        # by its digits, which lose nothing on the way
        return str(value)

    def _pyre_onDate(self, schema, value, **kwds):
        """
        Keep a date
        """
        # as the text sqlite keeps for it
        return value.isoformat()

    def _pyre_onTime(self, schema, value, **kwds):
        """
        Keep a time of day
        """
        # as the text sqlite keeps for it
        return value.isoformat()

    def _pyre_onTimestamp(self, schema, value, **kwds):
        """
        Keep a moment in time
        """
        # as the text sqlite keeps for it
        return value.isoformat(sep=" ")

    # implementation details
    def _numbered(self, index):
        """
        Render the placeholder of the value at {index}, counting from one
        """
        # by its number, so the values may be kept in any order
        return f"?{index}"

    def _typed(self, placeholder, cast):
        """
        Render {placeholder}, which stands for a value of type {cast}
        """
        # sqlite's values carry their own types, and its conversions would change them
        return placeholder


# end of file
