# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .StandardLiterals import StandardLiterals


# declaration
class PostgresLiterals(StandardLiterals):
    """
    Literals in the postgres dialect that are different from standard SQL
    """

    # public data
    dialect = "postgres"  # the name of the language, for the explanations of refusals
    emptyArray = "'{}'"  # the literal of an empty array, which takes the type of its column

    # strings of octets
    def _pyre_onBytes(self, schema, value, **kwds):
        """
        Render a string of octets
        """
        # as the hexadecimal digits postgres reads them from
        return f"'\\x{value.hex()}'"

    # identifiers
    def _pyre_onUUID(self, schema, value, **kwds):
        """
        Render a universally unique identifier
        """
        # as its canonical text, quoted
        return self.mill.quote(text=str(value))


# end of file
