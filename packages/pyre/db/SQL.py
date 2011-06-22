# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the text wrapping utilities
import textwrap
# my base class
from pyre.weaver.SQL import SQL as Mill


class SQL(Mill):
    """
    Generate SQL statements
    """


    def createTable(self, table):
        """
        Generate the SQL statement to create a database table given its description.

        The description in {table} is expected to be a subclass of {Table}, with the column
        information provided in the decorated column descriptors.
        """
        # the header
        yield self.place("CREATE TABLE " + table.pyre_name)
        # convert the table docstring into a comment block
        if table.__doc__:
            self.indent()
            for line in self.commentBlock(line.strip() for line in table.__doc__.splitlines()):
                yield line
            self.outdent()

        # start the declaration body
        yield self.place("(")

        # the terminator
        yield self.place(");")

        # all done
        return


    # implementation details


# end of file 
