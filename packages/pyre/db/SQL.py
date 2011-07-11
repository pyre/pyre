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

        # if there is a docstring
        if table.__doc__:
            # place the header
            yield self.place("CREATE TABLE " + table.pyre_name)
            # convert the docstring into a comment block
            self.indent()
            for line in self.commentBlock(line.strip() for line in table.__doc__.splitlines()):
                yield line
            self.outdent()
            # start the declaration body
            yield self.place("(")
        # otherwise
        else:
            # put it all on one line
            yield self.place("CREATE TABLE " + table.pyre_name + " (")

        # the column declarations
        self.indent()
        # how many?
        nColumns = len(table.pyre_columns)
        # iterate over the columns except the last one
        for index, column in enumerate(table.pyre_columns):
            # do we need a comma
            comma = (annotations > 0) or (index+1 < nColumns)
            # some declarations span multiple lines
            for line in self._columnDeclaration(column, comma):
                yield self.place(line)

        # if there are any table annotations
        if annotations:
            # separate the annotations with a blank line
            yield ""
            # the primary keys
            if len(table._pyre_primaryKeys):
                annotations -= 1
                yield self.place("PRIMARY KEY ({}){}".format(
                    ','.join(column.name for column in table._pyre_primaryKeys),
                    ',' if annotations else ''
                    ))
            # the unique constraints
            if len(table._pyre_uniqueColumns):
                annotations -= 1
                yield self.place("UNIQUE ({}){}".format(
                    ','.join(column.name for column in table._pyre_uniqueColumns),
                    ',' if annotations else ''
                    ))
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
                    yield self.place("FOREIGN KEY ({}) REFERENCES {} ({}){}".format(
                        local.column.name, foreign.table.pyre_name, foreign.column.name,
                        ',' if fkeys or annotations else ''
                        ))

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
                    yield self.place("CHECK ({}){}".format(
                        self.expression(root=constraint, table=table),
                        ',' if constraints or annotations else ''
                        ))

        # push out
        self.outdent()

        # the table declaration terminator
        yield self.place(");")

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

        # i get to render these as part of expressions
        from .ColumnReference import ColumnReference 
        # adjust the rendering strategy table
        self._renderers[ColumnReference] = self._columnReference

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
        # the column name
        name = column.name
        # the column type
        typedecl = column.decl()
        # default value if any
        default = column.decldefault()
        # compute the annotations
        annotations = []
        # a primary key
        if column._primary: annotations.append("PRIMARY KEY")
        # not null
        if column._notNull: annotations.append("NOT NULL")
        # unique
        if column._unique: annotations.append("UNIQUE")
        # assemble them
        annotations = " ".join(annotations)

        # is this a single line declaration
        oneLiner = not (annotations or column._foreign)
        # a column is "decorated" if it has annotations or is a foreign key declaration
        separator = ',' if (comma and oneLiner) else ''
        # is there a comment
        if column.doc:
            comment = ' ' + self.comment + ' ' + column.doc
        else:
            comment = ''

        # build the declaration line
        yield "{} {}{}{}{}".format(name, typedecl, default, separator, comment)
        # indent
        self.indent()

        # annotations
        if annotations:
            # comma?
            separator = ',' if (comma and not column._foreign) else ''
            yield annotations + separator
        # foreign keys
        if column._foreign:
            for line in self._referenceDeclaration(column._foreign, comma):
                yield line

        # all done
        self.outdent()
        return


    def _referenceDeclaration(self, foreign, comma):
        """
        Build a declaration for a foreign key
        """
        table = foreign.reference.table
        column = foreign.reference.column

        # comma?
        separator = ',' if comma and not (foreign.update or foreign.delete) else ''
        # build the reference line
        if column is None:
            yield "REFERENCES {.pyre_name}{}{}".format(table, separator)
        else:
            yield "REFERENCES {.pyre_name} ({.name}){}".format(table, column, separator)

        # if there is nothing further to do
        if foreign.update is None and foreign.delete is None:
            # move on
            return

        # otherwise
        self.indent()

        # if there is a registered update action
        if foreign.update:
            # comma?
            separator = ',' if (comma and not foreign.delete) else ''
            # record it
            yield "ON UPDATE {}{}".format(foreign.update, separator)
            
        # if there is a registered delete action
        if foreign.delete:
            # comma?
            separator = ',' if comma else ''
            # record it
            yield "ON DELETE {}{}".format(foreign.delete, separator)
            
        # all done
        self.outdent()
        return


# end of file 
