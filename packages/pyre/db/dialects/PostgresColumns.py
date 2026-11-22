# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .StandardColumns import StandardColumns


# declaration
class PostgresColumns(StandardColumns):
    """
    Type declarators in the postgres dialect that are different from standard SQL
    """

    # public data
    dialect = "postgres"  # the name of the language, for the explanations of refusals

    # text
    def _pyre_onString(self, schema, **kwds):
        """
        Spell the type of a column of text
        """
        # text of unbounded length
        if schema.maxlen is None:
            # has a type of its own
            return "TEXT"
        # the rest is spelled as standard SQL spells it
        return super()._pyre_onString(schema=schema, **kwds)

    # strings of octets
    def _pyre_onBytes(self, schema, **kwds):
        """
        Spell the type of a column of strings of octets
        """
        # postgres has a type of its own for them
        return "BYTEA"

    # identifiers
    def _pyre_onUUID(self, schema, **kwds):
        """
        Spell the type of a column of universally unique identifiers
        """
        # postgres has a type for them
        return "UUID"

    # arrays
    def _pyre_onArray(self, schema, table, column, **kwds):
        """
        Spell the type of a column of arrays
        """
        # the type of the entries
        entries = schema.schema._pyre_identify(authority=self, table=table, column=column)
        # marked as an array once, since postgres declares arrays of every rank alike
        return entries + " ARRAY"


# end of file
