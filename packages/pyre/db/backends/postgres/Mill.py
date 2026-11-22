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
class Mill(standard.Mill, family="pyre.db.dialects.postgres"):
    """
    Generate SQL statements in the dialect of postgres: standard SQL, except where postgres departs
    from it
    """

    # the name of my language, for the explanations of refusals
    dialect = "postgres"

    # the visitor that builds the type declarators of my columns
    columns = Columns
    # and the one that renders the literals of their values
    literals = Literals

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
