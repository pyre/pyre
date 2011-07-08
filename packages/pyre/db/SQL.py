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

    # types
    from .ColumnReference import ColumnReference # i get to render these as part of expressions


    # interface
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

        # does this table declaration have annotations past the column declarations?
        annotations = len(tuple(filter(None, [
            len(table._pyre_primaryKeys), len(table._pyre_foreignKeys),
            len(table._pyre_uniqueColumns), len(table._pyre_constraints) ])))

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

        # and the last one, which may not need the ',' separator
        for line in self._columnDeclaration(table.pyre_columns[-1], comma=annotations):
            yield self.leader + line

        # if there are any table annotations
        if annotations:
            # separate the annotations with a blank line
            yield ""
            # the primary keys
            if len(table._pyre_primaryKeys):
                annotations -= 1
                yield self.leader + "PRIMARY KEY ({}){}".format(
                    ','.join(column.name for column in table._pyre_primaryKeys),
                    ',' if annotations else ''
                    )
            # the unique constraints
            if len(table._pyre_uniqueColumns):
                annotations -= 1
                yield self.leader + "UNIQUE ({}){}".format(
                    ','.join(column.name for column in table._pyre_uniqueColumns),
                    ',' if annotations else ''
                    )
            # the foreign keys
            fkeys = len(table._pyre_foreignKeys)
            if fkeys:
                # update the annotation count
                annotations -= 1
                # go through each foreign key declaration
                for local, foreign in table._pyre_foreignKeys:
                    # update the key count
                    fkeys -= 1
                    # build the declaration
                    yield self.leader + "FOREIGN KEY ({}) REFERENCES {} ({}){}".format(
                        local.column.name, foreign.table.pyre_name, foreign.column.name,
                        ',' if fkeys or annotations else ''
                        )

            # the constraints
            constraints = len(table._pyre_constraints)
            if constraints:
                # update the annotation count
                annotations -= 1
                # go through each constraint
                for constraint in table._pyre_constraints:
                    # update the constraint count
                    constraints -= 1
                    # build the declaration
                    yield self.leader + "CHECK ({}){}".format(
                        self.expression(root=constraint, table=table),
                        ',' if constraints or annotations else ''
                        )

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


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)

        # adjust the rendering strategy table
        self._renderers[self.ColumnReference] = self._columnReference

        # and return
        return


    # implementation details
    def _columnReference(self, node, table, **kwds):
        """
        Render {node} as reference to a column
        """
        # if the reference is to a column in {table}
        if node.table == table:
            # skip the table name
            return node.column.name
        # otherwise, build a fully qualified reference
        return "{0.table.pyre_name}.{0.column.name}".format(node)


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
