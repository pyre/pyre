# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Visitor import Visitor


# declaration
class Columns(Visitor):
    """
    A visitor over table columns that generates type declarators in standard SQL.

    Types that are not supported by standard SQL are refused; dialects that provide support for
    non-standard types should provide subclasses that override the type relevant handlers.
    """

    # interface
    def declare(self, table, column):
        """
        Build the type declarator of {column}, a column of {table}
        """
        # let the column say what it is
        return column._pyre_identify(authority=self, table=table, column=column)

    def cast(self, schema):
        """
        Build the type declarator of {schema}, the target type of a conversion
        """
        # let the type say what it is
        return schema._pyre_identify(authority=self, usage="a cast to")

    # the columns whose values have no type in the language
    def _pyre_onSchema(self, schema, **kwds):
        """
        Refuse {column}, whose values the language has no type for
        """
        # complain
        raise self._refusal(contents="values", **kwds)

    # truth values
    def _pyre_onBoolean(self, schema, **kwds):
        """
        Build the type declarator of a column of truth values
        """
        # easy enough
        return "BOOLEAN"

    # numbers
    def _pyre_onInteger(self, schema, **kwds):
        """
        Build the type declarator of a column of integers
        """
        # easy enough
        return "INTEGER"

    def _pyre_onFloat(self, schema, **kwds):
        """
        Build the type declarator of a column of floating point numbers
        """
        # easy enough
        return "DOUBLE PRECISION"

    def _pyre_onDecimal(self, schema, **kwds):
        """
        Build the type declarator of a column of fixed point numbers
        """
        # with the number of their digits, and how many of them follow the point
        return f"DECIMAL({schema.precision}, {schema.scale})"

    # text
    def _pyre_onString(self, schema, **kwds):
        """
        Build the type declarator of a column of text
        """
        # text of unbounded length
        if schema.maxlen is None:
            # is a large object of characters
            return "CLOB"
        # the rest is bounded by its length
        return f"VARCHAR({schema.maxlen})"

    # strings of octets
    def _pyre_onBytes(self, schema, **kwds):
        """
        Build the type declarator of a column of strings of octets
        """
        # they are large objects of octets
        return "BLOB"

    # dates and times
    def _pyre_onDate(self, schema, **kwds):
        """
        Build the type declarator of a column of dates
        """
        # easy enough
        return "DATE"

    def _pyre_onTime(self, schema, **kwds):
        """
        Build the type declarator of a column of times of day
        """
        # a time of day carries its offset only when the column insists that it has one
        return "TIME WITH TIME ZONE" if schema.timezone is True else "TIME"

    def _pyre_onTimestamp(self, schema, **kwds):
        """
        Build the type declarator of a column of moments in time
        """
        # a moment carries its time zone only when the column insists that it has one
        return "TIMESTAMP WITH TIME ZONE" if schema.timezone is True else "TIMESTAMP"

    # identifiers
    def _pyre_onUUID(self, schema, **kwds):
        """
        Refuse a column of universally unique identifiers, which the language has no type for
        """
        # complain
        raise self._refusal(contents="identifiers", **kwds)

    # json documents
    def _pyre_onJSON(self, schema, **kwds):
        """
        Refuse a column of json documents, which the language has no type for
        """
        # complain
        raise self._refusal(contents="json documents", **kwds)

    # arrays
    def _pyre_onArray(self, schema, **kwds):
        """
        Build the type declarator of a column of arrays
        """
        # the type of the entries
        entries = schema.schema._pyre_identify(authority=self, **kwds)
        # the number of levels, which is one when the rank of the array is unknown
        levels = 1 if schema.rank is None else schema.rank
        # mark the type of the entries as an array once for each level
        return entries + " ARRAY" * levels


# end of file
