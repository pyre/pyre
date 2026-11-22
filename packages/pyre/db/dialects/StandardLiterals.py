# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the special value {NULL}
from .. import literals

# superclass
from .Visitor import Visitor


# declaration
class StandardLiterals(Visitor):
    """
    A visitor over table columns that renders their values as literals of standard SQL

    The form of each literal is fixed by the standard, so the literals are built from the values
    themselves; values of types that standard SQL does not support are refused, and dialects
    that support them provide subclasses that override the relevant handlers
    """

    # public data
    emptyArray = "ARRAY[]"  # the literal of an array without entries

    # interface
    def literal(self, table, column, value):
        """
        Render {value}, a value of {column} of {table}, as a literal
        """
        # {NULL} is the same whatever the column
        if value is literals.null:
            # so render it directly
            return "NULL"
        # otherwise, convert the value to the type of the column
        value = column.coerce(value=value)
        # and let the column say what it is
        return column._pyre_identify(authority=self, table=table, column=column, value=value)

    # the columns whose values have no type in the language
    def _pyre_onSchema(self, schema, **kwds):
        """
        Refuse a value of {column}, whose values the language has no type for
        """
        # complain
        raise self._refusal(contents="values", **kwds)

    # truth values
    def _pyre_onBoolean(self, schema, value, **kwds):
        """
        Render a truth value
        """
        # by its name
        return "TRUE" if value else "FALSE"

    # numbers
    def _pyre_onInteger(self, schema, value, **kwds):
        """
        Render an integer
        """
        # by its digits
        return str(value)

    def _pyre_onFloat(self, schema, value, **kwds):
        """
        Render a floating point number
        """
        # by its digits
        return str(value)

    def _pyre_onDecimal(self, schema, value, **kwds):
        """
        Render a fixed point number
        """
        # by its digits
        return str(value)

    # text
    def _pyre_onString(self, schema, value, **kwds):
        """
        Render a string
        """
        # quoted, as the language quotes text
        return self.mill.quote(text=value)

    # strings of octets
    def _pyre_onBytes(self, schema, value, **kwds):
        """
        Render a string of octets
        """
        # by its hexadecimal digits
        return f"X'{value.hex().upper()}'"

    # dates and times
    def _pyre_onDate(self, schema, value, **kwds):
        """
        Render a date
        """
        # in the form of the standard
        return f"DATE '{value.isoformat()}'"

    def _pyre_onTime(self, schema, value, **kwds):
        """
        Render a time of day
        """
        # in the form of the standard, with its offset when it has one
        return f"TIME '{value.isoformat()}'"

    def _pyre_onTimestamp(self, schema, value, **kwds):
        """
        Render a moment in time
        """
        # in the form of the standard, with its time zone when it has one
        return f"TIMESTAMP '{value.isoformat(sep=' ')}'"

    # identifiers
    def _pyre_onUUID(self, schema, **kwds):
        """
        Refuse a universally unique identifier, which the language has no type for
        """
        # complain
        raise self._refusal(contents="identifiers", **kwds)

    # arrays
    def _pyre_onArray(self, schema, value, **kwds):
        """
        Render an array
        """
        # level by level
        return self._level(schema=schema, level=value, **kwds)

    # implementation details
    def _level(self, schema, level, **kwds):
        """
        Render {level}, an entry or a level of an array of {schema}
        """
        # an entry
        if not isinstance(level, tuple):
            # is rendered by the column type of the entries
            return schema.schema._pyre_identify(authority=self, value=level, **kwds)
        # a level without entries
        if not level:
            # has a literal of its own
            return self.emptyArray
        # the others list what they hold
        return (
            "ARRAY["
            + ", ".join(self._level(schema=schema, level=entry, **kwds) for entry in level)
            + "]"
        )


# end of file
