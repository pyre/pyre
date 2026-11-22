# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my superclass
from ..standard import Mill as standard

# the type declarators of my columns
from .Columns import Columns

# and the literals of their values
from .Literals import Literals


# declaration
class Mill(standard.Mill, family="pyre.db.dialects.sqlite"):
    """
    Generate SQL statements in the dialect of sqlite: standard SQL, except where sqlite departs
    from it
    """

    # the name of my language, for the explanations of refusals
    dialect = "sqlite"

    # the visitor that builds the type declarators of my columns
    columns = Columns
    # and the one that renders the literals of their values
    literals = Literals

    # transactions
    def transaction(self):
        """
        Generate the SQL statement that initiates a transaction block
        """
        # every statement starts at the margin
        self.margin()
        # sqlite begins its transactions its own way
        yield self.place("BEGIN TRANSACTION;")
        # all done
        return

    # implementation details
    def _insertColumns(self, table, record):
        """
        Generate the columns of {table} that {record} names in an insert, with their values
        """
        # sqlite has no {DEFAULT} among the values of an insert
        for field, value in zip(table.pyre_fields, record):
            # so the columns left to their defaults
            if value is table.default:
                # are left out
                continue
            # and the others are named
            yield field, value
        # all done
        return


# end of file
