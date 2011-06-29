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


    def transaction(self):
        """
        Generate the SQL statement that initiates a transaction block
        """
        # simple enough
        yield "START TRANSACTION;"
        # all done
        return


    def commit(self):
        """
        Generate the SQL statement that closes a transaction block
        """
        # simple enough
        yield "COMMIT;"
        # all done
        return


    def rollback(self):
        """
        Generate the SQL statement that rolls back a transaction
        """
        # simple enough
        yield "ROLLBACK;"
        # all done
        return


    def createTable(self, table):
        """
        Generate the SQL statement to create a database table given its description.

        The description in {table} is expected to be a subclass of {Table}, with the column
        information provided in the decorated column descriptors.
        """
        # check that the table has columns
        if not table.pyre_columns:
            import journal
            error = journal.error("pyre.db.sql")
            error.log("table {!r} has no column information".format(table.pyre_name))
            return

        # the header
        yield self.place("CREATE TABLE " + table.pyre_name)
        # convert the table docstring into a comment block
        if table.__doc__:
            self.indent()
            for line in self.commentBlock(line.strip() for line in table.__doc__.splitlines()):
                yield line
            self.outdent()

        # start the declaration body
        yield self.leader + "("

        # the column declarations
        self.indent()
        # iterate over the columns except the last one
        for column in table.pyre_columns[:-1]:
            # some declarations span multiple lines
            for line in self._columnDeclaration(column, comma=True):
                yield self.leader + line

        # and the last one, which does  not need the ',' separator
        for line in self._columnDeclaration(table.pyre_columns[-1], comma=False):
            yield self.leader + line
        # push out
        self.outdent()

        # the table declaration terminator
        yield self.leader + ");"

        # all done
        return


    def dropTable(self, table):
        """
        Build the statement to drop the given {table}
        """
        # this is easy enogh
        yield "DROP TABLE {};".format(table.pyre_name)
        # all done
        return


    # implementation details
    def _columnDeclaration(self, column, comma):
        """
        Build the declaration lines for a given table column
        """
        # initialize the declaration
        declarator = [ column.name, column.decl(), column.decldefault() ]
        # terminate one liners
        if comma and not column._decorated:
            declarator.append(',')
        # add the docstring as a comment
        if column.doc:
            declarator += [self.comment, column.doc ]
        # render the name and type of the column
        yield " ".join(filter(None, declarator))

        # indent
        self.indent()

        # a primary key
        if column._primary: yield "PRIMARY KEY"
        # not null
        if column._notNull: yield "NOT NULL"
        # unique
        if column._unique: yield "UNIQUE"
        # foreign keys
        if column._foreign:
            for line in self._referenceDeclaration(column._foreign):
                yield line
        # render a column separator, if necessary 
        if comma and column._decorated:
            yield ','

        # all done
        self.outdent()
        return


    def _referenceDeclaration(self, foreign):
        """
        Build a declaration for a foreign key
        """
        table = foreign.reference.table
        column = foreign.reference.column
        if column is None:
            yield "REFERENCES {.pyre_name}".format(table)
        else:
            yield "REFERENCES {.pyre_name} ({.name})".format(table, column)

        # if there is nothing further to do
        if foreign.update is None and foreign.delete is None:
            # move on
            return

        # otherwise
        self.indent()

        # if there is a registered update action
        if foreign.update:
            # record it
            yield "ON UPDATE {}".format(foreign.update)
            
        # if there is a registered delete action
        if foreign.delete:
            # record it
            yield "ON DELETE {}".format(foreign.delete)
            
        # all done
        self.outdent()
        return


# end of file 
