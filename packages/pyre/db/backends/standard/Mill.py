# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import inspect
import collections.abc

# my base class
from pyre.weaver.SQL import SQL

# the local exceptions
from ... import exceptions

# the type declarators of my columns
from .Columns import Columns

# and the literals of their values
from .Literals import Literals


# declaration
class Mill(SQL, family="pyre.db.dialects.standard"):
    """
    Generate SQL statements in standard SQL
    """

    # constants
    INDENTER = " " * 2

    # the name of my language, for the explanations of refusals
    dialect = "standard SQL"
    # the words that make a creation conditional on the absence of what it creates, which the
    # language does not have
    ifMissing = None
    # and the words that make a removal conditional on the presence of what it removes, which it
    # does not have either
    ifPresent = None
    # whether the language has indexes, which it does not
    hasIndexes = False

    # the visitor that builds the type declarators of my columns, which each dialect replaces
    # with its own
    columns = Columns
    # and the one that renders the literals of their values
    literals = Literals

    # types
    # the metaclasses for tables and queries
    from ...schema.Schemer import Schemer as schemer
    from ...queries.Selector import Selector as selector

    # the base classes for tables and queries
    from ...schema.Table import Table as table
    from ...queries.Query import Query as query

    # queries
    def select(self, query):
        """
        Generate the SELECT statement described by {query}
        """
        # every statement starts at the margin
        self.margin()
        # start
        yield "SELECT"
        # prepare to render the field projection
        self.indent(increment=2)
        # if the query is a table specification
        if isinstance(query, self.schemer):
            # its columns
            fields = query.pyre_fields
            # name each of them
            for index, field in enumerate(fields):
                # do we need a comma?
                comma = "," if index + 1 < len(fields) else ""
                # read the column as the dialect reads it
                reading = self._read(column=field, text=field.name)
                # a reading other than the bare name of the column gets the name back
                alias = "" if reading == field.name else f" AS {field.name}"
                # render it
                yield self.place(f"{reading}{alias}{comma}")
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
                # read the field as the dialect reads it
                reading = self._read(column=entry, text=self.expression(entry))
                # and render it
                yield self.place(f"{reading} AS {entry.name}{comma}")
            # push out
            self.outdent()

            # the clauses that follow the {FROM} section, in the order the language puts them,
            # each with the method that renders it
            clauses = [
                (keyword, renderer)
                for keyword, spec, renderer in (
                    ("WHERE", query.where, self._whereClause),
                    ("GROUP BY", query.group, self._groupClause),
                    ("ORDER BY", query.order, self._orderClause),
                )
                # leaving out the ones the query does not have
                if spec is not None
            ]

            # render the {FROM} section
            yield self.place("FROM")
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
                elif not clauses:
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

            # render the clauses
            for index, (keyword, renderer) in enumerate(clauses):
                # the last one ends the statement
                terminator = ";" if index + 1 == len(clauses) else ""
                # push out
                self.outdent()
                # render the marker of the clause
                yield self.place(keyword)
                # push in
                self.indent()
                # and render its body
                yield self.place(renderer(query=query) + terminator)

            # push out
            self.outdent(decrement=2)
            # all done
            return

        # all done
        return

    # the reading of the columns of a selection
    def _read(self, column, text):
        """
        Render the reading of {column}, whose expression is {text}, in the projection of a selection
        """
        # the language reads every column as it is
        return text

    # the clauses of a selection
    def _whereClause(self, query):
        """
        Render the restriction of {query}
        """
        # build the filtering expression
        predicate = self.expression(root=query.where, context=query)
        # and put it in parentheses
        return f"({predicate})"

    def _groupClause(self, query):
        """
        Render the fields {query} groups its rows by
        """
        # render each of them
        return self._fieldList(query=query, spec=query.group)

    def _orderClause(self, query):
        """
        Render the order of the rows of {query}
        """
        # render each of its collations
        return self._fieldList(query=query, spec=query.order)

    def _fieldList(self, query, spec):
        """
        Render {spec}, one expression or several, in the context of {query}
        """
        # a single expression
        if not isinstance(spec, collections.abc.Iterable):
            # is a list of one
            spec = (spec,)
        # render each one, separated by commas
        return ", ".join(self.expression(root=entry, context=query) for entry in spec)

    # transaction support
    def transaction(self):
        """
        Generate the SQL statement that initiates a transaction block
        """
        # every statement starts at the margin
        self.margin()
        # simple enough
        yield self.place("START TRANSACTION;")
        # all done
        return

    def commit(self):
        """
        Generate the SQL statement that closes a transaction block
        """
        # every statement starts at the margin
        self.margin()
        # simple enough
        yield self.place("COMMIT;")
        # all done
        return

    def rollback(self):
        """
        Generate the SQL statement that rolls back a transaction
        """
        # every statement starts at the margin
        self.margin()
        # simple enough
        yield self.place("ROLLBACK;")
        # all done
        return

    # database management
    def createDatabase(self, name, existOk=False):
        """
        Refuse to create the database {name}, since the language has no statement for it
        """
        # complain
        raise exceptions.NotSupportedError(
            diagnostic=f"{self.dialect} has no statement that creates the database {name}"
        )

    def dropDatabase(self, name, missingOk=False):
        """
        Refuse to drop the database {name}, since the language has no statement for it
        """
        # complain
        raise exceptions.NotSupportedError(
            diagnostic=f"{self.dialect} has no statement that drops the database {name}"
        )

    # table management
    def createTable(self, table, existOk=False, indexes=True):
        """
        Generate the SQL statement to create a database table given its description, followed
        by those that create its indexes unless {indexes} is off; with {existOk}, finding the
        table and its indexes there already is fine

        The {table} specification is expected to be a {Table} subclass, with the necessary
        column information provided by the decorated field descriptors
        """
        # every statement starts at the margin
        self.margin()
        # if the table has no fields
        if not table.pyre_fields:
            # it's a bug
            import journal

            # so complain
            raise journal.firewall("pyre.db").log(
                f"table {table.pyre_name!r} has no field information"
            )

        # build the type declarator of each column before rendering anything, so that a column the
        # language has no type for leaves no part of the statement behind
        declarations = tuple(
            self._columns.declare(table=table, column=field) for field in table.pyre_fields
        )
        # and the declaration of the default of each column
        defaults = tuple(self._default(table=table, column=field) for field in table.pyre_fields)
        # and the declarations that follow the columns
        annotations = tuple(self._tableAnnotations(table=table))
        # the statements that record the documentation of the table in the catalog of the server
        notes = tuple(self._documentation(table=table))
        # and those that create its indexes, when they are wanted
        followers = tuple(self.createIndexes(table=table, existOk=existOk)) if indexes else ()
        # and the opening of the statement, which says whether the table may exist already
        header = (
            "CREATE TABLE"
            + self._ifMissing(existOk=existOk, subject=f"the table {table.pyre_name}")
            + f" {table.pyre_name}"
        )

        # if there is a docstring
        if table.__doc__:
            # place the header
            yield self.place(header)
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
            yield self.place(f"{header} (")

        # the field declarations
        self.indent()
        # how many?
        nFields = len(table.pyre_fields)
        # go through the fields
        for index, (field, declaration, default) in enumerate(
            zip(table.pyre_fields, declarations, defaults)
        ):
            # a comma, unless this is the last of the declarations
            comma = bool(annotations) or (index + 1 < nFields)
            # some declarations span multiple lines
            yield from self._fieldDeclaration(
                field=field, declaration=declaration, default=default, comma=comma
            )

        # if there are any table annotations
        if annotations:
            # separate them from the columns with a blank line
            yield ""
            # and render each one
            for index, annotation in enumerate(annotations):
                # followed by a comma, unless it is the last one
                yield self.place(annotation + ("," if index + 1 < len(annotations) else ""))
        # push out
        self.outdent()
        # the table declaration terminator
        yield self.place(");")
        # followed by the statements that record its documentation
        yield from notes
        # and those that create its indexes
        yield from followers
        # all done
        return

    def _tableAnnotations(self, table):
        """
        Generate the declarations that follow the columns of {table}: its keys, its references to
        other tables, and its checks
        """
        # the primary key, if there is one
        if table._pyre_primaryKeys:
            # names its fields, in order
            yield f"PRIMARY KEY ({','.join(field.name for field in table._pyre_primaryKeys)})"
        # each group of fields whose values are unique together
        for fields, name in table._pyre_uniqueKeys:
            # is a constraint of its own
            yield self._constraint(
                name=name, rule=f"UNIQUE ({','.join(field.name for field in fields)})"
            )
        # each reference to another table
        for local, foreign, name in table._pyre_foreignKeys:
            # names the field, the table, and the field of the other table
            yield self._constraint(
                name=name,
                rule=(
                    f"FOREIGN KEY ({local.field.name}) "
                    f"REFERENCES {foreign.table.pyre_name} ({foreign.field.name})"
                ),
            )
        # and each check
        for constraint, name in table._pyre_constraints:
            # renders its expression in the context of the table
            yield self._constraint(
                name=name, rule=f"CHECK ({self.expression(root=constraint, context=table)})"
            )
        # all done
        return

    def dropTable(self, table, missingOk=False):
        """
        Build the statement to drop the given {table}; with {missingOk}, finding it gone already is
        fine
        """
        # say whether the table may be gone already
        clause = self._ifPresent(missingOk=missingOk, subject=f"the table {table.pyre_name}")
        # every statement starts at the margin
        self.margin()
        # build the statement
        yield self.place(f"DROP TABLE{clause} {table.pyre_name};")
        # all done
        return

    # index management
    def createIndexes(self, table, existOk=False):
        """
        Build the statements that create the indexes of {table}; with {existOk}, finding them
        there already is fine
        """
        # each index
        for index in table._pyre_indexes:
            # gets a statement of its own
            yield from self._createIndex(table=table, index=index, existOk=existOk)
        # all done
        return

    def createIndex(self, table, name, existOk=False):
        """
        Build the statement that creates the index {name} of {table}; with {existOk}, finding it
        there already is fine
        """
        # find the index
        index = self._index(table=table, name=name)
        # and build its statement
        yield from self._createIndex(table=table, index=index, existOk=existOk)
        # all done
        return

    def dropIndex(self, table, name, missingOk=False):
        """
        Build the statement that drops the index {name} of {table}; with {missingOk}, finding it
        gone already is fine
        """
        # make sure {table} declares the index
        self._index(table=table, name=name)
        # a language without indexes
        if not self.hasIndexes:
            # cannot drop one
            raise exceptions.NotSupportedError(
                diagnostic=f"{self.dialect} has no statement that drops the index {name}"
            )
        # say whether the index may be gone already
        clause = self._ifPresent(missingOk=missingOk, subject=f"the index {name}")
        # every statement starts at the margin
        self.margin()
        # build the statement
        yield self.place(f"DROP INDEX{clause} {name};")
        # all done
        return

    # record management
    def insertRecords(self, *records):
        """
        Insert {records}, an iterable of table records, into their corresponding table; the
        consecutive records of a table that name the same columns share a statement
        """
        # every statement starts at the margin
        self.margin()
        # the values of the previous record, held back until we know whether more follow, so
        # that {records} can be a generator
        dangling = ""
        # the shape of the statement in progress, if any: its table and its columns
        shape = None
        # iterate over the records
        for record in records:
            # get the table of the record
            table = record.pyre_layout
            # the columns it names, with their values
            columns = tuple(self._insertColumns(table=table, record=record))
            # and its shape
            recordShape = (table, tuple(field.name for field, _ in columns))
            # a record of the same shape as the statement in progress
            if recordShape == shape:
                # joins it, so render the dangling values, followed by a comma
                yield self.place(dangling + ",")
            # the others
            else:
                # end the statement in progress, if there is one
                if shape is not None:
                    # by terminating it
                    yield self.place(dangling + ";")
                    # and bouncing out to the margin
                    self.outdent(decrement=2)
                # a record that names no column
                if not columns:
                    # is inserted by a statement of its own
                    yield self.place(f"INSERT INTO {table.pyre_name} DEFAULT VALUES;")
                    # which leaves no statement in progress
                    shape = None
                    # so move on
                    continue
                # the others start a statement of their shape
                shape = recordShape
                # initiate it
                yield self.place(f"INSERT INTO {table.pyre_name}")
                # indent
                self.indent(increment=2)
                # the names of the columns
                yield self.place("(" + ", ".join(recordShape[1]) + ")")
                # push out
                self.outdent()
                # start the section with the record values
                yield self.place("VALUES")
                # further in
                self.indent()
            # collect the values
            values = (
                self._recordValue(table=table, field=field, value=value) for field, value in columns
            )
            # render them
            dangling = "(" + ", ".join(values) + ")"

        # if there is no statement in progress
        if shape is None:
            # there is nothing left to render
            return
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
        # every statement starts at the margin
        self.margin()
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
        affected. Without a {condition}, every row is updated, and a {template} that sets no
        field builds no statement
        """
        # every statement starts at the margin
        self.margin()
        # get the table
        table = template.pyre_layout
        # the assignments, one for each field that {template} sets
        assignments = []
        # go through the fields
        for field in table.pyre_fields:
            # get the value in {template}
            value = getattr(template, field.name)
            # fields set to {None} are not affected
            if value is None:
                # so skip them
                continue
            # the others are assigned their value
            assignments.append(
                f"{field.name} = {self._recordValue(table=table, field=field, value=value)}"
            )
        # if there is nothing to set
        if not assignments:
            # there is no statement
            return

        # initiate the statement
        yield self.place(f"UPDATE {table.pyre_name}")
        # indent
        self.indent()
        # the data section
        yield self.place("SET")
        # indent
        self.indent()
        # render all assignments but the last, each followed by a comma
        for assignment in assignments[:-1]:
            # place it
            yield self.place(assignment + ",")
        # the last one ends the statement, unless a restriction follows
        yield self.place(assignments[-1] + ("" if condition is not None else ";"))
        # outdent
        self.outdent()
        # if there is a restriction
        if condition is not None:
            # build the filtering expression
            predicate = self.expression(root=condition, context=table)
            # and render it
            yield self.place(f"WHERE ({predicate});")
        # outdent
        self.outdent()
        # and return
        return

    # meta-methods
    def __init__(self, **kwds):
        # get the field definition
        from ... import field

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
        # a field of no table in particular, or of the table in context or one of its bases
        if not node.table or (isinstance(context, type) and issubclass(context, node.table)):
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
        # get the field, which is the one operand of the conversion
        (operand,) = node.operands
        # render it
        field = self.expression(root=operand, **kwds)
        # build the declarator of the target type
        target = self._columns.cast(schema=node.targetType)
        # and convert
        return f"CAST({field} AS {target})"

    def _pyre_onNegation(self, node, **kwds):
        """
        Render {node}, the negation of a predicate
        """
        # render the predicate
        predicate = self.expression(root=node.predicate, **kwds)
        # and negate it
        return f"NOT ({predicate})"

    def _pyre_onIsIn(self, node, **kwds):
        """
        Render {node}, the test of whether a field holds one of a list of values
        """
        # no field holds one of no values, and the language has no empty list to say it with
        if not node.values:
            # so say what it means
            return "FALSE"
        # render the field
        field = self.expression(root=node.field, **kwds)
        # and the literals of the values
        values = ", ".join(self._literals.value(value=value) for value in node.values)
        # put it all together
        return f"{field} IN ({values})"

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
    def _documentation(self, table):
        """
        Build the statements that record the documentation of {table} and its columns in the
        catalog of the server; the language has none, so the documentation stays in the comments
        of the statement that creates the table
        """
        # nothing to record
        return ()

    def _constraint(self, name, rule):
        """
        Build the declaration of a constraint of a table that enforces {rule}, under {name} when
        it has one
        """
        # a constraint without a name
        if name is None:
            # leaves its name to the server
            return rule
        # the others are declared by name
        return f"CONSTRAINT {name} {rule}"

    def _index(self, table, name):
        """
        Find the index of {table} whose name is {name}
        """
        # go through the indexes of the table
        for index in table._pyre_indexes:
            # and when one goes by {name}
            if index.identifier(table=table) == name:
                # hand it over
                return index
        # a name the table does not declare is a mistake in the code that asked for it
        import journal

        # so complain
        raise journal.firewall("pyre.db").log(
            f"table {table.pyre_name!r} declares no index {name!r}"
        )

    def _createIndex(self, table, index, existOk):
        """
        Build the statement that creates {index} of {table}; with {existOk}, finding it there
        already is fine
        """
        # the name of the index
        name = index.identifier(table=table)
        # a language without indexes
        if not self.hasIndexes:
            # cannot create one
            raise exceptions.NotSupportedError(
                diagnostic=f"{self.dialect} has no statement that creates the index {name}"
            )
        # say whether the index may exist already
        clause = self._ifMissing(existOk=existOk, subject=f"the index {name}")
        # whether no two rows may share their values
        unique = "UNIQUE " if index.unique else ""
        # the fields, in order
        fields = ", ".join(field.name for field in index.fields)
        # and the predicate a row must pass to be covered, if there is one
        where = (
            ""
            if index.where is None
            else f" WHERE ({self.expression(root=index.where, context=table)})"
        )
        # every statement starts at the margin
        self.margin()
        # build the statement
        yield self.place(
            f"CREATE {unique}INDEX{clause} {name} ON {table.pyre_name} ({fields}){where};"
        )
        # all done
        return

    def _ifMissing(self, existOk, subject):
        """
        Build the clause that lets the creation of {subject} find it there already, when {existOk}
        allows it
        """
        # a creation that insists on making {subject}
        if not existOk:
            # needs no clause
            return ""
        # a language without the words for the other kind
        if self.ifMissing is None:
            # cannot say it
            raise exceptions.NotSupportedError(
                diagnostic=(
                    f"{self.dialect} has no syntax that creates {subject} only when it is missing"
                )
            )
        # the rest have them
        return f" {self.ifMissing}"

    def _ifPresent(self, missingOk, subject):
        """
        Build the clause that lets the removal of {subject} find it gone already, when {missingOk}
        allows it
        """
        # a removal that insists on finding {subject}
        if not missingOk:
            # needs no clause
            return ""
        # a language without the words for the other kind
        if self.ifPresent is None:
            # cannot say it
            raise exceptions.NotSupportedError(
                diagnostic=(
                    f"{self.dialect} has no syntax that drops {subject} only when it is present"
                )
            )
        # the rest have them
        return f" {self.ifPresent}"

    def _literalRenderer(self, node, **kwds):
        """
        Render {node}, a literal in an expression, whose value belongs to no column
        """
        # the literal of its value depends only on the type of the value
        return self._literals.value(value=node._value)

    def _insertColumns(self, table, record):
        """
        Generate the columns of {table} that {record} names in an insert, with their values
        """
        # every column, in declaration order
        yield from zip(table.pyre_fields, record)
        # all done
        return

    def _recordValue(self, table, field, value):
        """
        Render {value}, the value of {field} in a record of {table}, for an insert or an update
        """
        # a missing value
        if value is None:
            # is left to the server in a column whose values it assigns, and is {NULL} elsewhere
            return "DEFAULT" if field._autogenerated else "NULL"
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
        # a column whose values the server assigns
        if column._autogenerated:
            # says so, along with whether a row may bring its own value
            return f" GENERATED {'BY DEFAULT' if column._supplied else 'ALWAYS'} AS IDENTITY"
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
