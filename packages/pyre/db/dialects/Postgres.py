# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my superclass
from .Standard import Standard

# the type declarators of my columns
from .PostgresColumns import PostgresColumns

# and the literals of their values
from .PostgresLiterals import PostgresLiterals


# declaration
class Postgres(Standard, family="pyre.db.dialects.postgres"):
    """
    Generate SQL statements in the dialect of postgres: standard SQL, except where postgres departs
    from it
    """

    # the name of my language, for the explanations of refusals
    dialect = "postgres"

    # the visitor that builds the type declarators of my columns
    columns = PostgresColumns
    # and the one that renders the literals of their values
    literals = PostgresLiterals

    # database management
    def createDatabase(self, name):
        """
        Generate the SQL statement to create the database {name}
        """
        # every statement starts at the margin
        self.margin()
        # simple enough
        yield self.place(f"CREATE DATABASE {name};")
        # all done
        return

    def dropDatabase(self, name):
        """
        Generate the SQL statement to drop the database {name}
        """
        # every statement starts at the margin
        self.margin()
        # simple enough
        yield self.place(f"DROP DATABASE {name};")
        # all done
        return


# end of file
