# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import datetime
import decimal
import uuid

# the special value {NULL}
from ...schema import literals

# superclass
from .Visitor import Visitor


# declaration
class Parameters(Visitor):
    """
    The values of a statement that travel beside it, rather than inside it as literals

    Each value is checked by the literals of the language, so a value they refuse is refused
    here too; it is then kept in the form the bindings of the back end take, and a placeholder
    takes its place in the statement. A value of a column takes a bare placeholder, which the
    column gives a type; a value that belongs to no column is cast to the type its literal would
    have carried, since nothing else says what it is
    """

    # the types of the values that belong to no column, by the type of the value
    types = {
        bool: "BOOLEAN",
        float: "DOUBLE PRECISION",
        decimal.Decimal: "NUMERIC",
        str: "CLOB",
        bytes: "BLOB",
        datetime.date: "DATE",
        datetime.time: "TIME",
        datetime.datetime: "TIMESTAMP",
    }
    # and of the integers, by the bits they need
    integers = ((32, "INTEGER"), (64, "BIGINT"))

    # interface
    def literal(self, table, column, value):
        """
        Keep {value}, a value of {column} of {table}, and render its placeholder
        """
        # {NULL} is the same whatever the column
        if value is literals.null:
            # so it is written as it is
            return "NULL"
        # let the literals refuse what the language has no type for
        self.mill._literals.literal(table=table, column=column, value=value)
        # convert the value to the type of the column
        value = column.coerce(value=value)
        # keep it in the form the bindings take
        self._values.append(
            column._pyre_identify(authority=self, table=table, column=column, value=value)
        )
        # and leave it to the column to give its placeholder a type
        return self._placeholder()

    def value(self, value):
        """
        Keep {value}, a value that belongs to no column, and render its placeholder
        """
        # {NULL} is the same whatever its type
        if value is None or value is literals.null:
            # so it is written as it is
            return "NULL"
        # let the literals refuse what the language has no literal for
        text = self.mill._literals.value(value=value)
        # the type of its placeholder
        cast = self._cast(value=value)
        # a value whose type a placeholder cannot carry
        if cast is None:
            # keeps its literal, which the literals have already checked
            return text
        # keep it in the form the bindings take
        self._values.append(self._handlers[type(value)](schema=None, value=value))
        # and render its placeholder, with its type
        return self._typed(placeholder=self._placeholder(), cast=cast)

    def drain(self):
        """
        Hand over the values kept since the last call, in the order of their placeholders, and
        start over, so the next statement numbers its placeholders from the first
        """
        # the values
        values = tuple(self._values)
        # start over
        self._values = []
        # and hand them over
        return values

    # the forms the bindings take, by the type of the column
    def _pyre_onSchema(self, schema, value, **kwds):
        """
        Keep a value as it is
        """
        # which is how the bindings take most values
        return value

    def _pyre_onBoolean(self, schema, value, **kwds):
        """
        Keep a truth value
        """
        # as it is
        return value

    def _pyre_onDecimal(self, schema, value, **kwds):
        """
        Keep a fixed point number
        """
        # as it is
        return value

    def _pyre_onDate(self, schema, value, **kwds):
        """
        Keep a date
        """
        # as it is
        return value

    def _pyre_onTime(self, schema, value, **kwds):
        """
        Keep a time of day
        """
        # as it is
        return value

    def _pyre_onTimestamp(self, schema, value, **kwds):
        """
        Keep a moment in time
        """
        # as it is
        return value

    def _pyre_onJSON(self, schema, value, **kwds):
        """
        Keep a json document
        """
        # as it is
        return value

    # implementation details
    def _placeholder(self):
        """
        Render the placeholder of the value kept last
        """
        # the language marks every placeholder the same way, and fills them in order
        return "?"

    def _typed(self, placeholder, cast):
        """
        Render {placeholder}, which stands for a value of type {cast}
        """
        # by converting it, which is how the language gives a placeholder a type
        return f"CAST({placeholder} AS {cast})"

    def _cast(self, value):
        """
        Build the type of the placeholder of {value}, a value that belongs to no column; a value
        whose type a placeholder cannot carry has none
        """
        # an integer
        if type(value) is int:
            # takes the narrowest type that holds it
            for bits, name in self.integers:
                # among those the language has
                if -(2 ** (bits - 1)) <= value < 2 ** (bits - 1):
                    # and that is the one
                    return name
            # integers wider than all of them are fixed point numbers without a fraction
            return "NUMERIC"
        # the others are looked up by their type
        return self.types.get(type(value))

    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the values of the statement in progress, in the order of their placeholders
        self._values = []
        # the forms the bindings take of the values that belong to no column, by their type
        self._handlers = {
            bool: self._pyre_onBoolean,
            int: self._pyre_onSchema,
            float: self._pyre_onSchema,
            decimal.Decimal: self._pyre_onDecimal,
            str: self._pyre_onSchema,
            bytes: self._pyre_onSchema,
            datetime.date: self._pyre_onDate,
            datetime.time: self._pyre_onTime,
            datetime.datetime: self._pyre_onTimestamp,
            uuid.UUID: self._pyre_onSchema,
            dict: self._pyre_onJSON,
        }
        # all done
        return


# end of file
