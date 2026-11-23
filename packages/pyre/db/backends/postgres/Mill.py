# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my superclass
from ..standard import Mill as standard

# the local exceptions
from ... import exceptions

# the columns of tables, and the references to them
from ...schema.Measure import Measure
from ...schema.FieldReference import FieldReference

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
    # the words that make a creation conditional on the absence of what it creates
    ifMissing = "IF NOT EXISTS"
    # and a removal conditional on the presence of what it removes
    ifPresent = "IF EXISTS"

    # the visitor that builds the type declarators of my columns
    columns = Columns
    # and the one that renders the literals of their values
    literals = Literals

    # the reading of the columns of a selection
    def _read(self, column, text):
        """
        Render the reading of {column}, whose expression is {text}, in the projection of a
        selection: a column marked to be read as its text is cast to it
        """
        # a reference to a column of a table
        if isinstance(column, FieldReference):
            # reads that column
            field = column.field
        # a column of a table
        elif isinstance(column, Measure):
            # reads itself
            field = column
        # anything else, such as a derivation
        else:
            # is read as it is
            return text
        # a column marked to be read as its text
        if field._asText:
            # is cast to it
            return f"{text}::text"
        # the others are read as they are
        return text

    # database management
    def createDatabase(self, name, existOk=False):
        """
        Generate the SQL statement to create the database {name}; postgres has no syntax that
        lets the statement find the database there already, so {existOk} is refused
        """
        # a creation that may find the database there already
        if existOk:
            # cannot be said in one statement
            raise exceptions.NotSupportedError(
                diagnostic=(
                    f"{self.dialect} has no syntax that creates the database {name}"
                    " only when it is missing"
                )
            )
        # every statement starts at the margin
        self.margin()
        # simple enough
        yield self.place(f"CREATE DATABASE {name};")
        # all done
        return

    def dropDatabase(self, name, missingOk=False):
        """
        Generate the SQL statement to drop the database {name}; with {missingOk}, finding it gone
        already is fine
        """
        # say whether the database may be gone already
        clause = self._ifPresent(missingOk=missingOk, subject=f"the database {name}")
        # every statement starts at the margin
        self.margin()
        # build the statement
        yield self.place(f"DROP DATABASE{clause} {name};")
        # all done
        return


# end of file
