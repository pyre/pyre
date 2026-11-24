# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import json
import math

# the special values {DEFAULT} and {NULL}
from ...schema import literals

# the local exceptions
from ... import exceptions


# declaration
class Text:
    """
    A visitor over table columns that writes their values in the text format of postgres's copies

    Each value is written as the text postgres reads for it, with the characters that would break
    a line or a row escaped by a backslash; a null is \\N, and the values of a row are separated
    by tabs, in the order its table declares its columns
    """

    # public data
    # the text of a null
    null = "\\N"
    # the characters that would break a line or a row, and their escapes
    escapes = str.maketrans({"\\": "\\\\", "\n": "\\n", "\r": "\\r", "\t": "\\t"})
    # and the characters that put an entry of an array in quotes: the ones the form of arrays
    # uses, and white space
    special = frozenset('{},"\\ \t\n\r\v\f')

    # interface
    def row(self, table, values):
        """
        Write {values}, the values of a row of {table} in the order of its columns, as a line,
        without its end
        """
        # each value in the text of its column, separated by tabs
        return "\t".join(
            self.value(table=table, column=column, value=value)
            for column, value in zip(table.pyre_fields, values)
        )

    def value(self, table, column, value):
        """
        Write {value}, a value of {column} of {table}, as its text, escaped
        """
        # a missing value, or {NULL}
        if value is None or value is literals.null:
            # is a null
            return self.null
        # otherwise, convert the value to the type of the column
        value = column.coerce(value=value)
        # let the column say what it is
        text = column._pyre_identify(authority=self, table=table, column=column, value=value)
        # and escape what would break the line
        return text.translate(self.escapes)

    # the columns whose values have no text
    def _pyre_onSchema(self, schema, **kwds):
        """
        Refuse a value of a column whose type has no text
        """
        # complain
        raise self._refusal(contents="values", **kwds)

    # truth values
    def _pyre_onBoolean(self, schema, value, **kwds):
        """
        Write a truth value
        """
        # as postgres writes it
        return "t" if value else "f"

    # numbers
    def _pyre_onInteger(self, schema, value, **kwds):
        """
        Write an integer
        """
        # by its digits
        return str(value)

    def _pyre_onFloat(self, schema, value, **kwds):
        """
        Write a floating point number
        """
        # a value that is not a number
        if math.isnan(value):
            # has a name
            return "NaN"
        # and so do the infinities
        if math.isinf(value):
            # which have a sign
            return "Infinity" if value > 0 else "-Infinity"
        # the others are written by the digits that read back as the same number
        return repr(value)

    def _pyre_onDecimal(self, schema, value, **kwds):
        """
        Write a fixed point number
        """
        # by its digits, or by the names of the values that are not numbers
        return str(value)

    # text
    def _pyre_onString(self, schema, value, **kwds):
        """
        Write a string
        """
        # as it is
        return value

    # strings of octets
    def _pyre_onBytes(self, schema, value, **kwds):
        """
        Write a string of octets
        """
        # by its hexadecimal digits, as postgres writes them
        return "\\x" + value.hex()

    # dates and times
    def _pyre_onDate(self, schema, value, **kwds):
        """
        Write a date
        """
        # in the form of the standard
        return value.isoformat()

    def _pyre_onTime(self, schema, value, **kwds):
        """
        Write a time of day
        """
        # in the form of the standard, with its offset when it has one
        return value.isoformat()

    def _pyre_onTimestamp(self, schema, value, **kwds):
        """
        Write a moment in time
        """
        # in the form of the standard, with its time zone when it has one
        return value.isoformat(sep=" ")

    # identifiers
    def _pyre_onUUID(self, schema, value, **kwds):
        """
        Write a universally unique identifier
        """
        # in its usual form
        return str(value)

    # json documents
    def _pyre_onJSON(self, schema, value, **kwds):
        """
        Write a json document
        """
        # a column read as its text
        if schema._asText:
            # holds the text of its documents
            return value
        # the others hold documents, which are written as their text
        return json.dumps(value, ensure_ascii=False)

    # arrays
    def _pyre_onArray(self, schema, value, **kwds):
        """
        Write an array, as postgres writes its arrays: each level in braces, its entries separated
        by commas, a null as NULL, and an entry that would be misread in double quotes
        """

        # the entries are values of the column type of the entries
        def entry(item):
            # a missing entry
            if item is None:
                # is a null
                return "NULL"
            # the others are written as their type says, and quoted when they need it
            return self._quoted(
                text=schema.schema._pyre_identify(authority=self, value=item, **kwds)
            )

        # write the array, level by level
        return self._level(level=value, entry=entry)

    # implementation details
    def _level(self, level, entry):
        """
        Write {level}, an entry or a level of an array whose entries are written by {entry}
        """
        # an entry
        if not isinstance(level, tuple):
            # is written as such
            return entry(level)
        # a level lists what it holds, in braces
        return "{" + ",".join(self._level(level=item, entry=entry) for item in level) + "}"

    def _quoted(self, text):
        """
        Put {text}, the text of an entry of an array, in double quotes when it would be misread
        without them: when it is empty, spells NULL, or holds a character the form of arrays uses
        """
        # text that reads back as itself
        if text and text.upper() != "NULL" and not any(c in self.special for c in text):
            # stays as it is
            return text
        # the others are quoted, with their quotes and backslashes escaped
        return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'

    def _refusal(self, contents, table, column, **kwds):
        """
        Build the exception that refuses {column} of {table}, whose {contents} a folder has no
        text for
        """
        # say what is wrong
        return exceptions.NotSupportedError(
            diagnostic=(
                f"the column {table.pyre_name}.{column.name} holds {contents},"
                " which a folder has no text for"
            ),
            table=table.pyre_name,
            column=column.name,
        )


# end of file
