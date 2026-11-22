# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import inspect
import collections.abc

# my base class
from pyre.weaver.SQL import SQL as Mill

# the local exceptions
from .. import exceptions

# the type declarators of my columns
from .StandardColumns import StandardColumns

# and the literals of their values
from .StandardLiterals import StandardLiterals


# declaration
class Standard(Mill, family="pyre.db.dialects.standard"):
    """
    Generate SQL statements in standard SQL
    """

    # constants
    INDENTER = " " * 2

    # the name of my language, for the explanations of refusals
    dialect = "standard SQL"

    # the visitor that builds the type declarators of my columns, which each dialect replaces
    # with its own
    columns = StandardColumns
    # and the one that renders the literals of their values
    literals = StandardLiterals

    # types
    # the metaclasses for tables and queries
    from ..Schemer import Schemer as schemer
    from ..Selector import Selector as selector

    # the base classes for tables and queries
    from ..Table import Table as table
    from ..Query import Query as query

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
        if isinstance(query, self.selector) or isinstance(query, self.query):
            # figure out how many field references there are
            fields = len(query.pyre_fields)
            # build the projection
            for index, entry in enumerate(query.pyre_fields):
                # do we need a comma?
                comma = "," if index + 1 < fields else ""
                # render this field
                yield self.place("{} AS {}{}".format(self.expression(entry), entry.name, comma))
            # push out
            self.outdent()

            # render the {FROM} section
            yield self.place("FROM")
            # do we have other clauses following the {FROM} section
            otherClauses = query.where or query.order or query.group
            # push in
            self.indent()
            # figure out how many table references there are
            tables = len(query.pyre_tables)
            # render the tables
            for index, tableName in enumerate(sorted(query.pyre_tables.keys())):
                # get the table
                table = query.pyre_tables[tableName]
                # do we need a terminator?
                # if we have more tables
                if index + 1 < tables:
                    # make it a comma
                    terminator = ","
                # if there are no other clauses in the query
                elif not otherClauses:
                    # wrap up
                    terminator = ";"
                # otherwise
                else:
                    # leave blank
                    terminator = ""
                # do we need to rename the table?
                if tableName == table.pyre_name:
                    # no
                    yield self.place("{}{}".format(table.pyre_name, terminator))
                # otherwise
                else:
                    # build a local alias for the table name
                    yield self.place("{} AS {}{}".format(table.pyre_name, tableName, terminator))

            # render the {WHERE} clause
            if query.where is not None:
                # do we have other clauses following the {FROM} section
                otherClauses = query.order or query.group
                # build a terminator
                terminator = "" if otherClauses else ";"
                # push out
                self.outdent()
                # build the filtering expression
                predicate = self.expression(root=query.where, context=query)
                # render the {WHERE} marker
                yield self.place("WHERE")
                # push in
                self.indent()
                # and render the expression
                yield self.place("({}){}".format(predicate, terminator))

            # render the {ORDER BY} clause
            order = query.order
            # if it exists
            if order is not None:
                # if it is not an iterable
                if not isinstance(order, collections.abc.Iterable):
                    # make it one
                    order = (order,)
                # push out
                self.outdent()
                # render the {ORDER BY} marker
                yield self.place("ORDER BY")
                # push in
                self.indent()
                # build the collation expression
                collation = (self.expression(root=spec, context=query) for spec in order)
                # and render it
                yield self.place("{};".format(", ".join(collation)))

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
        Refuse to create the database {name}, since the language has no statement for it
        """
        # complain
        raise exceptions.NotSupportedError(
            diagnostic=f"{self.dialect} has no statement that creates the database {name}"
        )

    def dropDatabase(self, name):
        """
        Refuse to drop the database {name}, since the language has no statement for it
        """
        # complain
        raise exceptions.NotSupportedError(
            diagnostic=f"{self.dialect} has no statement that drops the database {name}"
        )

    # table management
    def createTable(self, table):
        """
        Generate the SQL statement to create a database table given its description

        The {table} specification is expected to be a {Table} subclass, with the necessary
        column information provided by the decorated field descriptors
        """
        # if the table has no fields
        if not table.pyre_fields:
            # it's a bug
            import journal

            # so complain
            raise journal.firewall("pyre.db").log(
                "table {.pyre_name!r} has no field information".format(table)
            )

        # count the kinds of table annotations that follow the field declarations
        annotations = len(
            tuple(
                filter(
                    None,
                    [
                        len(table._pyre_primaryKeys),
                        len(table._pyre_foreignKeys),
                        len(table._pyre_uniqueFields),
                        len(table._pyre_constraints),
                    ],
                )
            )
        )

        # build the type declarator of each column before rendering anything, so that a column the
        # language has no type for leaves no part of the statement behind
        declarations = tuple(
            self._columns.declare(table=table, column=field) for field in table.pyre_fields
        )
        # and the declaration of the default of each column
        defaults = tuple(self._default(table=table, column=field) for field in table.pyre_fields)

        # if there is a docstring
        if table.__doc__:
            # place the header
            yield self.place("CREATE TABLE " + table.pyre_name)
            # push in
            self.indent()
            # convert the docstring into a comment block, framed by blank lines
            yield from self.commentBlock(["", *inspect.cleandoc(table.__doc__).splitlines(), ""])
            # push out
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
        # go through the fields
        for index, (field, declaration, default) in enumerate(
            zip(table.pyre_fields, declarations, defaults)
        ):
            # do we need a comma
            comma = (annotations > 0) or (index + 1 < nFields)
            # some declarations span multiple lines
            yield from self._fieldDeclaration(
                field=field, declaration=declaration, default=default, comma=comma
            )

        # if there are any table annotations
        if annotations:
            # separate the annotations with a blank line
            yield ""
            # the primary keys
            if len(table._pyre_primaryKeys):
                # update the annotation count
                annotations -= 1
                # build the declaration, with a comma if more annotations follow
                yield self.place(
                    "PRIMARY KEY ({}){}".format(
                        ",".join(field.name for field in table._pyre_primaryKeys),
                        "," if annotations else "",
                    )
                )
            # the unique constraints
            if len(table._pyre_uniqueFields):
                # update the annotation count
                annotations -= 1
                # build the declaration, with a comma if more annotations follow
                yield self.place(
                    "UNIQUE ({}){}".format(
                        ",".join(field.name for field in table._pyre_uniqueFields),
                        "," if annotations else "",
                    )
                )
            # the foreign keys
            fkeys = len(table._pyre_foreignKeys)
            # if there are any
            if fkeys:
                # update the annotation count
                annotations -= 1
                # go through each foreign key declaration
                for local, foreign in table._pyre_foreignKeys:
                    # update the key count
                    fkeys -= 1
                    # build the declaration
                    yield self.place(
                        "FOREIGN KEY ({}) REFERENCES {} ({}){}".format(
                            local.field.name,
                            foreign.table.pyre_name,
                            foreign.field.name,
                            "," if fkeys or annotations else "",
                        )
                    )

            # the constraints
            constraints = len(table._pyre_constraints)
            # if there are any
            if constraints:
                # update the annotation count
                annotations -= 1
                # go through each constraint
                for constraint in table._pyre_constraints:
                    # update the constraint count
                    constraints -= 1
                    # build the declaration
                    yield self.place(
                        "CHECK ({}){}".format(
                            self.expression(root=constraint, context=table),
                            "," if constraints or annotations else "",
                        )
                    )
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
        # this is easy enough
        yield "DROP TABLE {};".format(table.pyre_name)
        # all done
        return

    # record management
    def insertRecords(self, *records):
        """
        Insert {records}, an iterable of table records, into their corresponding table
        """
        # the values of the previous record, held back until we know whether more follow, so
        # that {records} can be a generator
        dangling = ""
        # the table whose records are being inserted
        table = None
        # iterate over the records
        for record in records:
            # check whether this record is from the table we are processing, if any
            if record.pyre_layout is not table:
                # if we are in the middle of a statement
                if table is not None:
                    # terminate the statement
                    yield self.place(dangling + ";")
                    # outdent
                    self.outdent().outdent()
                # in any case, save the target table
                table = record.pyre_layout
                # initiate the statement
                yield self.place("INSERT INTO {}".format(table.pyre_name))
                # indent
                self.indent(increment=2)
                # the field names in declaration order
                yield self.place(
                    "({})".format(", ".join(field.name for field in table.pyre_fields))
                )
                # push out
                self.outdent()
                # start the section with the record values
                yield self.place("VALUES")
                # further in
                self.indent()
            # otherwise
            else:
                # render any dangling values
                yield self.place(dangling + ",")  # add a comma since we know there are more...
            # collect the values
            values = (
                self._recordValue(table=table, field=field, value=value)
                for field, value in zip(table.pyre_fields, record)
            )
            # render them
            dangling = "({})".format(", ".join(values))

        # render any left overs
        yield self.place(dangling + ";")
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
        predicate = self.expression(root=condition, context=table)
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
        # get the table
        table = template.pyre_layout
        # the names of the affected fields
        names = []
        # and their values
        values = []
        # iterate over all the fields
        for field in table.pyre_fields:
            # get the corresponding name from {template}
            name = field.name
            # and the value
            value = getattr(template, name)
            # fields set to {None} are not affected
            if value is None:
                # so skip them
                continue

            # this field needs an update, so record its name
            names.append(name)
            # and its value
            values.append(self._recordValue(table=table, field=field, value=value))

        # render the names
        names = "(" + ", ".join(names) + ")"
        # and the values
        values = "(" + ", ".join(values) + ")"

        # initiate the statement
        yield self.place("UPDATE {}".format(table.pyre_name))
        # indent
        self.indent()
        # the data section
        yield self.place("SET")
        # indent
        self.indent()
        # render the assignments
        yield self.place("{} = {}".format(names, values))
        # outdent
        self.outdent()
        # build the filtering expression
        predicate = self.expression(root=condition, context=table)
        # and render it
        yield self.place("WHERE ({});".format(predicate))
        # outdent
        self.outdent()
        # and return
        return

    # meta-methods
    def __init__(self, **kwds):
        # get the field definition
        from .. import field

        # chain up
        super().__init__(nodeType=field, **kwds)

        # build the visitor of the type declarators of my columns
        self._columns = self.columns(mill=self)
        # and the one of the literals of their values, which quotes text as i do
        self._literals = self.literals(mill=self)

        # all done
        return

    # expressions
    def _pyre_onFieldReference(self, node, context=None, **kwds):
        """
        Render {node}, a reference to a field
        """
        # a reference that names no field
        if node.field is None:
            # refers to the whole table
            return node.table.pyre_name
        # a field of no table in particular, or of the table in context
        if not node.table or context is node.table:
            # is named by itself
            return node.field.name
        # any other is qualified by the name of its table
        return f"{node.table.pyre_name}.{node.field.name}"

    def _pyre_onCollation(self, node, context=None, **kwds):
        """
        Render {node}, the order in which the values of a field are sorted
        """
        # NYI: i would like to be able to trim the fully qualified table reference for fields
        # that are locally aliased in the current query; see the test
        # {query_collation_explicit} for an example: the {ORDER BY} expression should just
        # mention {date}, rather {weather.date}

        # render the field
        field = self.expression(root=node.fieldref, context=context, **kwds)
        # and mark it with its order
        return f"{field} {node.collation}"

    def _pyre_onIsNull(self, node, **kwds):
        """
        Render {node}, the test of whether a field is {NULL}
        """
        # render the operand
        operand = self.expression(root=node.operand, **kwds)
        # and test it
        return f"{operand} IS NULL"

    def _pyre_onIsNotNull(self, node, **kwds):
        """
        Render {node}, the test of whether a field is anything but {NULL}
        """
        # render the operand
        operand = self.expression(root=node.operand, **kwds)
        # and test it
        return f"{operand} IS NOT NULL"

    def _pyre_onCast(self, node, **kwds):
        """
        Render {node}, the conversion of the value of a field to another type
        """
        # render the field
        field = self.expression(root=node.field, **kwds)
        # build the declarator of the target type
        target = self._columns.cast(schema=node.targetType)
        # and convert
        return f"CAST({field} AS {target})"

    def _pyre_onLike(self, node, **kwds):
        """
        Render {node}, the match of a field against a pattern, naming the character that escapes
        its wildcards, since the back ends disagree on what it is when it is left out
        """
        # render the field
        field = self.expression(root=node.field, **kwds)
        # quote the pattern
        pattern = self.quote(text=node.pattern)
        # and the escape character
        escape = self.quote(text=node.escape)
        # put it all together
        return f"({field} LIKE {pattern} ESCAPE {escape})"

    # implementation details
    def _literalRenderer(self, node, **kwds):
        """
        Render {node}, a literal in an expression, whose value belongs to no column
        """
        # the literal of its value depends only on the type of the value
        return self._literals.value(value=node._value)

    def _recordValue(self, table, field, value):
        """
        Render {value}, the value of {field} in a record of {table}, for an insert or an update
        """
        # a missing value
        if value is None:
            # is {NULL}
            return "NULL"
        # the special values {DEFAULT} and {NULL}
        if value is table.default or value is table.null:
            # render as themselves
            return value.value
        # everything else is a literal of its column
        return self._literals.literal(table=table, column=field, value=value)

    def _default(self, table, column):
        """
        Build the declaration of the default of {column} of {table}, if it has one
        """
        # a column without a default
        if column.default is None:
            # declares none
            return ""
        # the others declare the literal of theirs
        return " DEFAULT " + self._literals.literal(
            table=table, column=column, value=column.default
        )

    def _fieldDeclaration(self, field, declaration, default, comma):
        """
        Build the declaration lines for a given table field, whose type declarator is
        {declaration} and whose default is declared by {default}
        """
        # the field name
        name = field.name
        # compute the annotations
        annotations = []
        # if the field is a primary key
        if field._primary:
            # say so
            annotations.append("PRIMARY KEY")
        # if it may not be null
        if field._notNull:
            # say so
            annotations.append("NOT NULL")
        # if its values must be unique
        if field._unique:
            # say so
            annotations.append("UNIQUE")
        # assemble them
        annotations = " ".join(annotations)

        # a field with annotations or a foreign key spans several lines
        oneLiner = not (annotations or field._foreign)
        # so its first line gets the comma only when it is the whole declaration
        separator = "," if (comma and oneLiner) else ""
        # if the field is documented
        if field.doc:
            # place its documentation in a comment at the end of the line
            comment = " " + self.comment + " " + field.doc
        # otherwise
        else:
            # leave the comment out
            comment = ""

        # build the declaration line
        yield self.place(f"{name} {declaration}{default}{separator}{comment}")
        # indent
        self.indent()

        # annotations
        if annotations:
            # get the comma, unless a foreign key follows
            separator = "," if (comma and not field._foreign) else ""
            # render them
            yield self.place(annotations + separator)
        # foreign keys
        if field._foreign:
            # render
            yield from self._referenceDeclaration(field._foreign, comma)

        # push out
        self.outdent()
        # all done
        return

    def _referenceDeclaration(self, foreign, comma):
        """
        Build a declaration for a foreign key
        """
        # the table being referenced
        table = foreign.reference.table
        # and its field, if any
        field = foreign.reference.field

        # the reference line gets the comma, unless actions follow
        separator = "," if comma and not (foreign.update or foreign.delete) else ""
        # if the reference names no field, it is to the primary key of the table
        if field is None:
            # so name only the table
            yield self.place("REFERENCES {.pyre_name}{}".format(table, separator))
        # otherwise
        else:
            # name the table and the field
            yield self.place("REFERENCES {.pyre_name} ({.name}){}".format(table, field, separator))

        # if there is nothing further to do
        if foreign.update is None and foreign.delete is None:
            # move on
            return

        # otherwise, push in
        self.indent()

        # if there is a registered update action
        if foreign.update:
            # comma?
            separator = "," if (comma and not foreign.delete) else ""
            # record it
            yield self.place("ON UPDATE {}{}".format(foreign.update, separator))

        # if there is a registered delete action
        if foreign.delete:
            # comma?
            separator = "," if comma else ""
            # record it
            yield self.place("ON DELETE {}{}".format(foreign.delete, separator))

        # push out
        self.outdent()
        # all done
        return


# end of file
