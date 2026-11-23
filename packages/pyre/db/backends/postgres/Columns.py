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
    Type declarators in the postgres dialect that are different from standard SQL
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

    # strings of octets
    def _pyre_onBytes(self, schema, **kwds):
        """
        Build the type declarator of a column of strings of octets
        """
        # postgres has a type of its own for them
        return "BYTEA"

    # identifiers
    def _pyre_onUUID(self, schema, **kwds):
        """
        Build the type declarator of a column of universally unique identifiers
        """
        # postgres has a type for them
        return "UUID"

    # json documents
    def _pyre_onJSON(self, schema, **kwds):
        """
        Build the type declarator of a column of json documents
        """
        # postgres keeps them in a binary form of its own, unless the column asks for their text
        return "JSON" if schema._verbatim else "JSONB"

    # arrays
    def _pyre_onArray(self, schema, **kwds):
        """
        Build the type declarator of a column of arrays
        """
        # the type of the entries
        entries = schema.schema._pyre_identify(authority=self, **kwds)
        # marked as an array once, since postgres declares arrays of every rank alike
        return entries + " ARRAY"


# end of file
