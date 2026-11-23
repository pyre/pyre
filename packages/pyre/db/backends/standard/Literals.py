# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import datetime
import decimal
import math
import uuid

# the special value {NULL}
from ...schema import literals

# the local exceptions
from ... import exceptions

# superclass
from .Visitor import Visitor


# declaration
class Literals(Visitor):
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

    def value(self, value):
        """
        Render {value}, a value that belongs to no column, as a literal
        """
        # {NULL} is the same whatever its type
        if value is None or value is literals.null:
            # so render it directly
            return "NULL"
        # look up the handler of the type of the value
        try:
            # among the types that have literals
            handler = self._handlers[type(value)]
        # a value of any other type has no literal
        except KeyError:
            # so get the name of its type
            name = type(value).__name__
            # and say what the language cannot write
            raise exceptions.NotSupportedError(
                diagnostic=f"{self.dialect} has no literal for values of type {name}"
            ) from None
        # let the handler render it
        return handler(schema=None, value=value, usage="a literal of")

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
        # a value that is not a number
        if math.isnan(value):
            # has a literal only in some dialects
            return self._notANumber(**kwds)
        # and so do the infinities
        if math.isinf(value):
            # which have a sign
            return self._infinity(positive=value > 0, **kwds)
        # the others are written by their digits
        return str(value)

    def _pyre_onDecimal(self, schema, value, **kwds):
        """
        Render a fixed point number
        """
        # a value that is not a number
        if value.is_nan():
            # has a literal only in some dialects
            return self._notANumber(**kwds)
        # and so do the infinities
        if value.is_infinite():
            # which have a sign
            return self._infinity(positive=value > 0, **kwds)
        # the others are written by their digits
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

    # json documents
    def _pyre_onJSON(self, schema, **kwds):
        """
        Refuse a json document, which the language has no type for
        """
        # complain
        raise self._refusal(contents="json documents", **kwds)

    # arrays
    def _pyre_onArray(self, schema, value, **kwds):
        """
        Render an array, a value of a column
        """

        # its entries are values of the column type of the entries
        def entry(value):
            # so let that type say what each one is
            return schema.schema._pyre_identify(authority=self, value=value, **kwds)

        # render it level by level
        return self._array(level=value, entry=entry, **kwds)

    def _valueArray(self, schema, value, **kwds):
        """
        Render a tuple, a value that belongs to no column, as an array
        """
        # its entries belong to no column either, so render it level by level
        return self._array(level=value, entry=self.value, **kwds)

    # implementation details
    def _notANumber(self, **kwds):
        """
        Refuse a value that is not a number, which the language has no literal for
        """
        # complain
        raise self._unwritable(name="not a number", **kwds)

    def _infinity(self, positive, **kwds):
        """
        Refuse an infinity, {positive} or not, which the language has no literal for
        """
        # complain
        raise self._unwritable(name="infinity", **kwds)

    def _unwritable(self, name, table=None, column=None, **kwds):
        """
        Build the exception that refuses a value the language has no literal for, as {name}
        describes it
        """
        # the table the value belongs to, when it belongs to one
        tableName = "" if table is None else table.pyre_name
        # and its column
        columnName = "" if column is None else column.name
        # say what the language cannot write
        return exceptions.NotSupportedError(
            diagnostic=f"{self.dialect} has no literal for {name}",
            table=tableName,
            column=columnName,
        )

    def _array(self, level, entry, **kwds):
        """
        Render {level}, an entry or a level of an array whose entries are rendered by {entry}
        """
        # an entry
        if not isinstance(level, tuple):
            # is rendered as such
            return entry(value=level)
        # a level without entries
        if not level:
            # has a literal of its own
            return self.emptyArray
        # the others list what they hold
        return (
            "ARRAY["
            + ", ".join(self._array(level=item, entry=entry, **kwds) for item in level)
            + "]"
        )

    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the handlers of the values that belong to no column, by the type of the value
        self._handlers = {
            bool: self._pyre_onBoolean,
            int: self._pyre_onInteger,
            float: self._pyre_onFloat,
            decimal.Decimal: self._pyre_onDecimal,
            str: self._pyre_onString,
            bytes: self._pyre_onBytes,
            datetime.date: self._pyre_onDate,
            datetime.time: self._pyre_onTime,
            datetime.datetime: self._pyre_onTimestamp,
            uuid.UUID: self._pyre_onUUID,
            tuple: self._valueArray,
            dict: self._pyre_onJSON,
        }
        # all done
        return


# end of file
