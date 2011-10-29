# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# iterator tools
import itertools
# access to the text wrapping utilities
import textwrap
# my base class
from pyre.weaver.SQL import SQL as Mill


class SQL(Mill, family="pyre.db.sql"):
    """
    Generate SQL statements
    """


    # constants
    INDENTER = " "*2

    # types
    # the metaclasses for tables and queries
    from .Schemer import Schemer as schemer
    from .Selector import Selector as selector
    # the base classes for tables and queries
    from .Table import Table as table
    from .Query import Query as query


    # interface
    # queries
    def select(self, query):
        """
        Generate the SELECT statement described by {query}
        """
        # start
        yield "SELECT"
        # prepare to render the field projection
        self.indent(increment=2)
        # if the query is a table specification
        if isinstance(query, self.schemer):
            # no projection
            yield self.place("*")
            # push out
            self.outdent()
            # render the table name
            yield self.place("FROM {};".format(query.pyre_name))
            # push out
            self.outdent()
            # all done
            return

        # native queries
        if isinstance(query, self.selector):
            # do we have other clauses following the {FROM} section
            otherClauses = False
            # figure out how many field references there are
            fields = len(query.pyre_fields)
            # build the projection
            for index, (alias, expr) in enumerate(query.pyre_fields):
                # do we need a comma?
                comma = ',' if index+1 < fields else ''
                # render this field
                yield self.place("{} AS {}{}".format(self.expression(expr), alias, comma))
            # push out
            self.outdent()
            # render the {FROM} section
            yield self.place("FROM")
            # push in
            self.indent()
            # figure out how many table references there are
            tables = len(query.pyre_tables)
            # render the tables
            for index, table in enumerate(sorted(query.pyre_tables, key=lambda x: x.pyre_name)):
                # do we need a terminator?
                # if we have more tables
                if index + 1 < tables: 
                    # make it a comma
                    terminator = ','
                # if there are no other clauses in the query
                elif not otherClauses:
                    terminator = ';'
                # otherwise
                else:
                    # leave blank
                    terminator = ''
                # do we need to rename the table?
                if table.pyre_alias == table.pyre_name:
                    # no
                    yield self.place("{}{}".format(table.pyre_alias, terminator))
                # otherwise
                else:
                    # build a local alias for the table name
                    yield self.place("{} AS {}{}".format(
                            table.pyre_alias, table.pyre_name, terminator))

            # push out
            self.outdent(decrement=2)
            # all done
            return

        # all done
        return


    # transaction support
    def transaction(self):
        """
        Generate the SQL statement that initiates a transaction block
        """
        # simple enough
        yield self.place("START TRANSACTION;")
        # all done
        return


    def commit(self):
        """
        Generate the SQL statement that closes a transaction block
        """
        # simple enough
        yield self.place("COMMIT;")
        # all done
        return


    def rollback(self):
        """
        Generate the SQL statement that rolls back a transaction
        """
        # simple enough
        yield self.place("ROLLBACK;")
        # all done
        return


    # database management
    def createDatabase(self, name):
        """
        Generate the SQL statement to create the database {name}
        """
        # simple enough
        yield self.place("CREATE DATABASE {};".format(name))
        # all done
        return


    def dropDatabase(self, name):
        """
        Generate the SQL statement to drop the database {name}
        """
        # simple enough
        yield self.place("DROP DATABASE {};".format(name))
        # all done
        return


    # table management
    def createTable(self, table):
        """
        Generate the SQL statement to create a database table given its description.

        The description in {table} is expected to be a subclass of {Table}, with the field
        information provided in the decorated field descriptors.
        """
        # check that the table has fields
        if not table.pyre_fields:
            import journal
            error = journal.error("pyre.db.sql")
            error.log("table {!r} has no field information".format(table.pyre_name))
            return

        # does this table declaration have annotations past the field declarations?
        annotations = len(tuple(filter(None, [
            len(table._pyre_primaryKeys), len(table._pyre_foreignKeys),
            len(table._pyre_uniqueFields), len(table._pyre_constraints) ])))

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

        # the field declarations
        self.indent()
        # how many?
        nFields = len(table.pyre_fields)
        # iterate over the fields except the last one
        for index, field in enumerate(table.pyre_fields):
            # do we need a comma
            comma = (annotations > 0) or (index+1 < nFields)
            # some declarations span multiple lines
            for line in self._fieldDeclaration(field, comma):
                yield self.place(line)

        # if there are any table annotations
        if annotations:
            # separate the annotations with a blank line
            yield ""
            # the primary keys
            if len(table._pyre_primaryKeys):
                annotations -= 1
                yield self.place("PRIMARY KEY ({}){}".format(
                    ','.join(field.name for field in table._pyre_primaryKeys),
                    ',' if annotations else ''
                    ))
            # the unique constraints
            if len(table._pyre_uniqueFields):
                annotations -= 1
                yield self.place("UNIQUE ({}){}".format(
                    ','.join(field.name for field in table._pyre_uniqueFields),
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
                        local.field.name, foreign.table.pyre_name, foreign.field.name,
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


    # record management
    def insertRecords(self, *records):
        """
        Insert {records}, an iterable of table records, into their corresponding table
        """
        # markers
        dangling = "" # a bit of complexity to support {records} as generators
        targetTable = None
        # iterate over the records
        for record in records:
            # check whether this record is from the table we are processing, if any
            if record.__class__ is not targetTable:
                # if we are in the middle of a statement
                if targetTable is not None:
                    # terminate the statement
                    yield self.place(dangling + ";")
                    # outdent
                    self.outdent().outdent()
                # in any case, save the target table
                targetTable = record.__class__
                # initiate the statement
                yield self.place("INSERT INTO {}".format(record.pyre_name))
                # indent
                self.indent(increment=2)
                # the field names in declaration order
                yield self.place("({})".format(
                        ", ".join(field.name for field in record.pyre_fields)))
                # start the section with the record values
                self.outdent()
                yield self.place("VALUES")
                # further in
                self.indent()
            # otherwise
            else:
                # render any dangling values
                yield self.place(dangling + ',') # add a comma since we know there are more...
            # render the record values
            dangling = "({})".format(record.pyre_toSQL())

        # render any left overs
        yield self.place(dangling + ';')
        # bounce out to top level
        self.outdent(decrement=2)
        # all done
        return


    def deleteRecords(self, table, condition):
        """
        Remove all {table} records that match {condition}

        If condition is {None}, this routine will remove all records from the given {table}
        """
        # if no condition was specified
        if condition is None:
            # delete all records
            yield self.place("DELETE FROM {};".format(table.pyre_name))
            # all done
            return

        # otherwise, initiate the statement
        yield self.place("DELETE FROM {}".format(table.pyre_name))
        # indent
        self.indent()
        # build the filtering expression
        predicate = self.expression(root=condition, table=table)
        # and render it
        yield self.place("WHERE ({});".format(predicate))
        # outdent
        self.outdent()
        # and return
        return


    def updateRecords(self, template, condition):
        """
        Update all table rows that match {condition} using information from {template}, a
        prototype row of a table. The update operation sets the fields in these rows to their
        corresponding values in {template}; fields set to {None} in {template} are not
        affected.
        """
        # build the tuple of affected fields and their values
        names = []
        values = []
        # by iterating over all the fields
        for field in template.pyre_fields:
            # getting the corresponding name from {template}
            name = field.name
            value = getattr(template, name)
            # skipping the ones set to {None}
            if value is None: continue
            # and saving the rest
            names.append(name)
            values.append(value)

        # render the names
        names = "(" + ", ".join(names) + ")"
        values = tuple(values)

        # initiate the statement
        yield self.place("UPDATE {}".format(template.pyre_name))
        # indent
        self.indent()
        # the data section
        yield self.place("SET")
        # indent
        self.indent()
        # render the assignments
        yield self.place("{} = {!r}".format(names, values))
        # outdent
        self.outdent()
        # build the filtering expression
        predicate = self.expression(root=condition, table=template.__class__)
        # and render it
        yield self.place("WHERE ({});".format(predicate))
        # outdent
        self.outdent()
        # and return
        return


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)

        # i get to render these as part of expressions
        from .FieldReference import FieldReference 
        # adjust the rendering strategy table
        self._renderers[FieldReference] = self._fieldReference

        # and return
        return


    # implementation details
    def _fieldReference(self, node, table=None, **kwds):
        """
        Render {node} as reference to a field
        """
        # if the reference is to a field in {table}
        if table is not None and node.table == table:
            # skip the table name
            return node.field.name
        # otherwise, build a fully qualified reference
        return "{0.table.pyre_name}.{0.field.name}".format(node)


    def _fieldDeclaration(self, field, comma):
        """
        Build the declaration lines for a given table field
        """
        # the field name
        name = field.name
        # the field type
        typedecl = field.decl()
        # default value if any
        default = field.decldefault()
        # compute the annotations
        annotations = []
        # a primary key
        if field._primary: annotations.append("PRIMARY KEY")
        # not null
        if field._notNull: annotations.append("NOT NULL")
        # unique
        if field._unique: annotations.append("UNIQUE")
        # assemble them
        annotations = " ".join(annotations)

        # is this a single line declaration
        oneLiner = not (annotations or field._foreign)
        # a field is "decorated" if it has annotations or is a foreign key declaration
        separator = ',' if (comma and oneLiner) else ''
        # is there a comment
        if field.doc:
            comment = ' ' + self.comment + ' ' + field.doc
        else:
            comment = ''

        # build the declaration line
        yield "{} {}{}{}{}".format(name, typedecl, default, separator, comment)
        # indent
        self.indent()

        # annotations
        if annotations:
            # comma?
            separator = ',' if (comma and not field._foreign) else ''
            yield annotations + separator
        # foreign keys
        if field._foreign:
            for line in self._referenceDeclaration(field._foreign, comma):
                yield line

        # all done
        self.outdent()
        return


    def _referenceDeclaration(self, foreign, comma):
        """
        Build a declaration for a foreign key
        """
        table = foreign.reference.table
        field = foreign.reference.field

        # comma?
        separator = ',' if comma and not (foreign.update or foreign.delete) else ''
        # build the reference line
        if field is None:
            yield "REFERENCES {.pyre_name}{}".format(table, separator)
        else:
            yield "REFERENCES {.pyre_name} ({.name}){}".format(table, field, separator)

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
