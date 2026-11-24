# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import collections.abc
import inspect
import operator
import re

# my base class
from pyre.weaver.SQL import SQL

# the types of values
from pyre import schemata

# the local exceptions
from ... import exceptions

# the slots for the values of prepared statements
from ...schema.Parameter import Parameter

# the words the language reserves
from . import keywords

# the type declarators of my columns
from .Columns import Columns

# and the literals of their values
from .Literals import Literals

# and the values of statements that travel beside them
from .Parameters import Parameters


# declaration
class Mill(SQL, family="pyre.db.dialects.standard"):
    """
    Generate SQL statements in standard SQL
    """

    # constants
    INDENTER = " " * 2

    # the name of my language, for the explanations of refusals
    dialect = "standard SQL"
    # the words it reserves, which a name must be quoted to use
    reserved = keywords.reserved
    # and the shape of the names it reads as they are
    plain = re.compile(r"[a-z_][a-z0-9_]*")
    # the words that make a creation conditional on the absence of what it creates, which the
    # language does not have
    ifMissing = None
    # and the words that make a removal conditional on the presence of what it removes, which it
    # does not have either
    ifPresent = None
    # whether the language has indexes, which it does not
    hasIndexes = False
    # whether a statement may return the rows it changes, which it may not either
    hasReturning = False
    # and whether an insert may meet the rows that are there already, which it may not, so the
    # language merges them instead
    hasConflict = False
    # what may happen to the rows that are there already
    existingRows = ("keep", "replace")
    # whether the language says so when an insert keeps the values a row brings for a column
    # whose values the server assigns
    hasOverriding = True
    # what may happen to those values, which are refused unless they are kept
    generatedValues = ("keep",)
    # whether the language can add a reference to a table that exists already
    addsReferences = True
    # and the type of the bounds of a selection, which are numbers of rows; the value of a slot
    # that stands for one takes it
    rowCount = schemata.int()

    # the visitor that builds the type declarators of my columns, which each dialect replaces
    # with its own
    columns = Columns
    # and the one that renders the literals of their values
    literals = Literals
    # and the one that keeps the values of a statement that travel beside it
    placeholders = Parameters

    # types
    # the metaclasses for tables and queries
    from ...schema.Schemer import Schemer as schemer
    from ...queries.Selector import Selector as selector

    # the base classes for tables and queries
    from ...schema.Table import Table as table
    from ...queries.Query import Query as query

    # and for the joins of queries
    from ...queries.Join import Join as join

    # the references to the fields of tables
    from ...schema.FieldReference import FieldReference as fieldReference

    # the values that travel beside a statement
    def parameters(self):
        """
        Make a place for the values of a statement, which keeps them in the form the bindings of
        the back end take, and writes a placeholder in the statement in place of each
        """
        # make one that works for me
        return self.placeholders(mill=self)

    # queries
    def select(self, query, limit=None, offset=None, parameters=None):
        """
        Generate the SELECT statement described by {query}; {offset} skips that many of the
        first rows, and {limit} keeps at most that many of the rest, and either may be a slot of
        a prepared statement; with {parameters}, the values in the statement are kept there, and
        placeholders take their place
        """
        # only integers and slots may reach the statement as the bounds of the selection: the
        # limit
        limit = self._bound(value=limit)
        # and the offset
        offset = self._bound(value=offset)
        # every statement starts at the margin
        self.margin()
        # the clauses that page through the rows, as the dialect writes them, rendered after the
        # rest of the selection, so that their values are kept in the order of the text
        paging = self._paging(limit=limit, offset=offset, parameters=parameters)
        # build the statement
        lines = list(self._selection(query=query, paging=paging, parameters=parameters))
        # end its last line
        lines[-1] += ";"
        # and hand it over
        yield from lines
        # all done
        return

    def _selection(self, query, paging, parameters=None):
        """
        Generate the lines of the selection described by {query}, followed by the clauses in
        {paging}, without the terminator of the statement; its values go to {parameters}, when
        it is given
        """
        # if the query is a table specification
        if isinstance(query, self.schemer):
            # start
            yield "SELECT"
            # prepare to render the columns
            self.indent(increment=2)
            # its columns
            fields = query.pyre_fields
            # name each of them
            for index, field in enumerate(fields):
                # do we need a comma?
                comma = "," if index + 1 < len(fields) else ""
                # read the column as the dialect reads it
                reading = self._read(column=field, text=self.identifier(field.name))
                # a reading other than the bare name of the column gets the name back
                alias = (
                    ""
                    if reading == self.identifier(field.name)
                    else f" AS {self.identifier(field.name)}"
                )
                # render it
                yield self.place(f"{reading}{alias}{comma}")
            # push out
            self.outdent()
            # render the table name
            yield self.place(f"FROM {self.identifier(query.pyre_name)}")
            # followed by the paging
            for line in paging:
                # one clause at a time
                yield self.place(line)
            # push out
            self.outdent()
            # all done
            return

        # anything else must be a native query
        if not (isinstance(query, self.selector) or isinstance(query, self.query)):
            # which is a mistake in the code that asked
            import journal

            # so complain
            raise journal.firewall("pyre.db").log(f"{query!r} is neither a table nor a query")

        # start, asking for distinct rows when the query wants them
        yield "SELECT DISTINCT" if query.distinct else "SELECT"
        # prepare to render the field projection
        self.indent(increment=2)
        # figure out how many field references there are
        fields = len(query.pyre_fields)
        # build the projection
        for index, entry in enumerate(query.pyre_fields):
            # do we need a comma?
            comma = "," if index + 1 < fields else ""
            # read the field as the dialect reads it
            reading = self._read(
                column=entry, text=self.expression(root=entry, parameters=parameters)
            )
            # and render it
            yield self.place(f"{reading} AS {self.identifier(entry.name)}{comma}")
        # push out
        self.outdent()

        # the joins of the query, in their order
        joins = self._joins(query=query)
        # the names of the tables they join
        joined = {join.table.pyre_name for join in joins}
        # and the names of the others, in order
        names = [name for name in sorted(query.pyre_tables) if name not in joined]

        # render the {FROM} section
        yield self.place("FROM")
        # push in
        self.indent()
        # render the tables that are not joined
        for index, name in enumerate(names):
            # the reference to the table
            reference = self._tableReference(query=query, name=name)
            # in a query with joins, which read from left to right
            if joins:
                # the tables after the first are crossed with the ones before them
                yield self.place(reference if index == 0 else f"CROSS JOIN {reference}")
            # otherwise
            else:
                # they are separated by commas
                yield self.place(reference + ("," if index + 1 < len(names) else ""))
        # followed by the joins
        for join in joins:
            # the reference to the table
            reference = self._tableReference(query=query, name=join.table.pyre_name)
            # the predicate its rows must satisfy
            predicate = self.expression(root=join.on, context=query, parameters=parameters)
            # put it all together
            yield self.place(f"{join.keyword} {reference} ON ({predicate})")

        # the clauses that follow the {FROM} section, in the order the language puts them, each
        # with the method that renders it
        clauses = (
            ("WHERE", query.where, self._whereClause),
            ("GROUP BY", query.group, self._groupClause),
            ("ORDER BY", query.order, self._orderClause),
        )
        # go through them
        for keyword, spec, renderer in clauses:
            # leaving out the ones the query does not have
            if spec is None:
                # by moving on
                continue
            # push out
            self.outdent()
            # render the marker of the clause
            yield self.place(keyword)
            # push in
            self.indent()
            # and render its body
            yield self.place(renderer(query=query, parameters=parameters))

        # back out to the level of the clauses
        self.outdent()
        # where the paging goes
        for line in paging:
            # one clause at a time
            yield self.place(line)
        # push out
        self.outdent()
        # all done
        return

    def _returning(self, returning):
        """
        Build the clause that returns the columns of {returning}, a table or a query, from the
        rows a statement changes
        """
        # a language without the clause
        if not self.hasReturning:
            # cannot say it
            raise exceptions.NotSupportedError(
                diagnostic=f"{self.dialect} has no syntax that returns the rows a statement changes"
            )
        # the others name the columns
        return "RETURNING " + ", ".join(
            self.identifier(field.name) for field in returning.pyre_fields
        )

    def _insertEnd(self, values, tail):
        """
        End an insert whose last row of {values} is held back, followed by the clauses in
        {tail}, pairs of a depth below the level of the clauses and a line
        """
        # without clauses
        if not tail:
            # the values end the statement
            yield self.place(values + ";")
            # and that's all
            return
        # otherwise, the values are followed
        yield self.place(values)
        # by the clauses, at the level of the others
        self.outdent()
        # each one
        for index, (depth, line) in enumerate(tail):
            # the last of which ends the statement
            terminator = ";" if index + 1 == len(tail) else ""
            # at its depth
            self.indent(increment=depth)
            # placed
            yield self.place(line + terminator)
            # and back
            self.outdent(decrement=depth)
        # and back in, where the caller expects to be
        self.indent()
        # all done
        return

    def _insertTail(self, shape, existing, key, clause):
        """
        Build the clauses that follow the values of an insert of {shape}, a table and the names
        of its columns: what happens to the rows that are there already, and what the
        statement returns
        """
        # the clauses, as pairs of a depth and a line
        tail = []
        # an insert that may meet the rows that are there already
        if existing is not None:
            # unpack the shape
            table, names = shape
            # find the key that detects them
            keys = self._conflictKey(table=table, key=key)
            # the columns to write over the row that is there
            assignments = (
                [name for name in names if name not in keys] if existing == "replace" else []
            )
            # the clause that detects the row
            conflict = f"ON CONFLICT ({', '.join(self.identifier(key) for key in keys)})"
            # with nothing to write over it
            if not assignments:
                # the row is left alone
                tail.append((0, f"{conflict} DO NOTHING"))
            # otherwise
            else:
                # the row is updated
                tail.append((0, f"{conflict} DO UPDATE SET"))
                # with the value of each column
                for index, name in enumerate(assignments):
                    # each but the last followed by a comma
                    comma = "," if index + 1 < len(assignments) else ""
                    # taken from the row that was refused
                    tail.append(
                        (1, f"{self.identifier(name)} = EXCLUDED.{self.identifier(name)}{comma}")
                    )
        # the rows the statement returns
        if clause is not None:
            # come last
            tail.append((0, clause))
        # hand them over
        return tail

    def _conflictKey(self, table, key):
        """
        Find the names of the fields of {table} that detect the rows that are there already:
        those of {key}, a field or a sequence of them, or those of the primary key
        """
        # without a key
        if key is None:
            # the fields of the primary key of the table
            fields = list(table._pyre_primaryKeys) or [
                field for field in table.pyre_fields if field._primary
            ]
            # are the key
            names = [field.name for field in fields]
        # otherwise
        else:
            # take the fields of the key, in order
            references = (key,) if isinstance(key, self.fieldReference) else tuple(key)
            # and their names
            names = [reference.field.name for reference in references]
            # of the table of the records
            if any(not issubclass(table, reference.table) for reference in references):
                # or the key is a mistake in the code that asked
                names = []
        # a table without a key
        if not names:
            # cannot tell which rows are there already, which is a mistake in the code that asked
            import journal

            # so complain
            raise journal.firewall("pyre.db").log(
                f"there is no key of table {table.pyre_name!r} that finds the rows that are there"
            )
        # hand them over
        return names

    def _merge(self, records, existing, key, parameters=None, generated=None):
        """
        Merge {records} into their tables, keeping or replacing the rows that are there already,
        as {existing} asks; the consecutive records of a table that give the same columns share a
        statement, and each statement is handed over whole; their values go to {parameters},
        when it is given, and the values they bring for the columns the server assigns are kept
        when {generated} asks for it
        """
        # the groups of records of the same shape
        groups = []
        # go through the records
        for record in records:
            # get the table of the record
            table = record.pyre_layout
            # the columns it gives values for, with their values
            columns = tuple(self._givenColumns(table=table, record=record))
            # whether the insert must take the values the record brings over the server's own
            overriding = self._overriding(table=table, columns=columns, generated=generated)
            # and its shape
            shape = (table, tuple(field for field, _ in columns), overriding)
            # a record of the same shape as the last group
            if groups and groups[-1][0] == shape:
                # joins it
                groups[-1][1].append(columns)
            # otherwise
            else:
                # it starts a group of its own
                groups.append((shape, [columns]))
        # each group
        for (table, fields, overriding), rows in groups:
            # is merged by a statement of its own
            yield tuple(
                self._mergeStatement(
                    table=table,
                    fields=fields,
                    rows=rows,
                    existing=existing,
                    key=key,
                    parameters=parameters,
                    overriding=overriding,
                )
            )
        # all done
        return

    def _mergeStatement(
        self, table, fields, rows, existing, key, parameters=None, overriding=False
    ):
        """
        Build the statement that merges {rows} into {table}, each giving values for {fields};
        with {overriding}, the rows that are inserted keep the values they bring for the columns
        the server assigns
        """
        # the names of the columns
        names = [field.name for field in fields]
        # the key that detects the rows that are there already
        keys = self._conflictKey(table=table, key=key)
        # must be among the columns the rows give
        if any(name not in names for name in keys):
            # or the rows cannot be matched, which is a mistake in the code that asked
            import journal

            # so complain
            raise journal.firewall("pyre.db").log(
                f"the rows merged into table {table.pyre_name!r} give no value for its key"
            )
        # every statement starts at the margin
        self.margin()
        # the target
        yield self.place(f"MERGE INTO {self.identifier(table.pyre_name)}")
        # indent
        self.indent()
        # the source
        yield self.place("USING (")
        # indent
        self.indent()
        # is a list of rows
        yield self.place("VALUES")
        # indent
        self.indent()
        # each one
        for index, columns in enumerate(rows):
            # with its values
            values = ", ".join(
                self._recordValue(table=table, field=field, value=value, parameters=parameters)
                for field, value in columns
            )
            # each but the last followed by a comma
            yield self.place(f"({values})" + ("," if index + 1 < len(rows) else ""))
        # back out
        self.outdent(decrement=2)
        # name the source and its columns
        yield self.place(f") AS incoming ({', '.join(self.identifier(name) for name in names)})")
        # match the rows on the key
        match = " AND ".join(
            f"{self.identifier(table.pyre_name)}.{self.identifier(name)}"
            f" = incoming.{self.identifier(name)}"
            for name in keys
        )
        # and say so
        yield self.place(f"ON ({match})")
        # the columns to write over the rows that are there
        assignments = [name for name in names if name not in keys] if existing == "replace" else []
        # when there are any
        if assignments:
            # the matched rows are updated
            yield self.place("WHEN MATCHED THEN UPDATE SET")
            # indent
            self.indent()
            # with the value of each column
            for index, name in enumerate(assignments):
                # each but the last followed by a comma
                comma = "," if index + 1 < len(assignments) else ""
                # taken from the incoming row
                yield self.place(
                    f"{self.identifier(name)} = incoming.{self.identifier(name)}{comma}"
                )
            # back out
            self.outdent()
        # the others are inserted
        yield self.place(
            f"WHEN NOT MATCHED THEN INSERT ({', '.join(self.identifier(name) for name in names)})"
        )
        # indent
        self.indent()
        # rows that bring values for the columns the server assigns
        if overriding:
            # have them taken over the server's own
            yield self.place("OVERRIDING SYSTEM VALUE")
        # with the values of the incoming row
        sources = ", ".join(f"incoming.{self.identifier(name)}" for name in names)
        # which ends the statement
        yield self.place(f"VALUES ({sources});")
        # back out to the margin
        self.outdent(decrement=2)
        # all done
        return

    def _generatedRequest(self, generated):
        """
        Make sure {generated}, a request about the values of the columns the server assigns, is
        one the language knows
        """
        # a request that is not one of them
        if generated is not None and generated not in self.generatedValues:
            # is a mistake in the code that made it
            import journal

            # so complain
            raise journal.firewall("pyre.db").log(
                f"the values of the columns the server assigns may be kept, not {generated!r}"
            )
        # all done
        return

    def _overriding(self, table, columns, generated):
        """
        Decide whether an insert of {columns}, fields of {table} with their values, must say that
        it keeps the values they bring for columns whose values the server assigns; such a value
        is refused unless {generated} asks to keep it
        """
        # the columns whose values the server assigns, takes from no row, and are given one
        assigned = [
            field
            for field, value in columns
            if field._autogenerated
            and not field._supplied
            and value is not None
            and value is not table.default
        ]
        # without any
        if not assigned:
            # the server's own values stand
            return False
        # values that are not to be kept
        if generated != "keep":
            # are a mistake of the caller
            raise exceptions.InterfaceError(
                diagnostic=(
                    f"a value was given for the column {table.pyre_name}.{assigned[0].name},"
                    " whose values the server assigns"
                )
            )
        # the others are kept, which a language that has the words for it must say
        return self.hasOverriding

    def _givenColumns(self, table, record):
        """
        Generate the columns of {table} that {record} gives values for, with their values,
        leaving out those it leaves to the server
        """
        # go through the columns, in declaration order
        for field, value in zip(table.pyre_fields, record):
            # the columns left to their defaults, and those whose values the server assigns
            # that have none
            if value is table.default or (field._autogenerated and value is None):
                # are left out
                continue
            # and the others are given
            yield field, value
        # all done
        return

    def _subquery(self, query, parameters=None):
        """
        Render the selection of {query}, a query of one column, on a single line, to stand for a
        list of values; its values go to {parameters}, when it is given
        """
        # a query of several columns
        if len(query.pyre_fields) != 1:
            # cannot stand for a list of values, which is a mistake in the code that asked
            import journal

            # so complain
            raise journal.firewall("pyre.db").log(
                f"query {query.pyre_name!r} selects {len(query.pyre_fields)} columns,"
                " so it cannot stand for a list of values"
            )
        # render its selection, without paging
        lines = self._selection(query=query, paging=(), parameters=parameters)
        # and put it on one line
        return " ".join(line.strip() for line in lines)

    def _joins(self, query):
        """
        Collect the joins of {query}, making sure each joins one of its tables
        """
        # the joins of the query: none
        if query.joins is None:
            # makes an empty pile
            return ()
        # one join
        if isinstance(query.joins, self.join):
            # makes a pile of one
            joins = (query.joins,)
        # and the rest are piles already
        else:
            # so take them in their order
            joins = tuple(query.joins)
        # go through them
        for join in joins:
            # and if one joins a table the query does not name
            if join.table.pyre_name not in query.pyre_tables:
                # it is a mistake in the declaration of the query
                import journal

                # so complain
                raise journal.firewall("pyre.db").log(
                    f"query {query.pyre_name!r} joins the table {join.table.pyre_name!r},"
                    " which is not among its tables"
                )
        # hand them over
        return joins

    def _tableReference(self, query, name):
        """
        Render the reference to the table that {query} knows as {name}
        """
        # get the table
        table = query.pyre_tables[name]
        # a table under its own name
        if name == table.pyre_name:
            # is named as it is
            return self.identifier(table.pyre_name)
        # the others get a local alias
        return f"{self.identifier(table.pyre_name)} AS {self.identifier(name)}"

    def _paging(self, limit, offset, parameters=None):
        """
        Generate the clauses that skip the first {offset} rows of a selection and keep at most
        {limit} of the rest, as the language writes them; a bound that is a slot goes to
        {parameters}, when it is given
        """
        # skipping rows, which comes first
        if offset is not None:
            # says how many
            yield f"OFFSET {self._count(value=offset, parameters=parameters)} ROWS"
        # and keeping some
        if limit is not None:
            # says how many
            yield f"FETCH FIRST {self._count(value=limit, parameters=parameters)} ROWS ONLY"
        # all done
        return

    def _bound(self, value):
        """
        Check {value}, a bound of a selection, which is a number of rows, a slot that stands for
        one, or missing
        """
        # a missing bound, and a slot, whose value is checked when the statement runs
        if value is None or isinstance(value, Parameter):
            # are left as they are
            return value
        # anything else must be an integer
        return operator.index(value)

    def _count(self, value, parameters=None):
        """
        Render {value}, a bound of a selection, which is a number of rows or a slot that stands
        for one; a slot goes to {parameters}, when it is given
        """
        # a slot
        if isinstance(value, Parameter):
            # is rendered by whoever keeps the values of the statement
            writer = self._literals if parameters is None else parameters
            # as a number of rows
            return writer.countSlot(parameter=value)
        # a number is written by its digits
        return str(value)

    # the reading of the columns of a selection
    def _read(self, column, text):
        """
        Render the reading of {column}, whose expression is {text}, in the projection of a selection
        """
        # the language reads every column as it is
        return text

    # the clauses of a selection
    def _whereClause(self, query, parameters=None):
        """
        Render the restriction of {query}, whose values go to {parameters}, when it is given
        """
        # build the filtering expression
        predicate = self.expression(root=query.where, context=query, parameters=parameters)
        # and put it in parentheses
        return f"({predicate})"

    def _groupClause(self, query, parameters=None):
        """
        Render the fields {query} groups its rows by, whose values go to {parameters}, when it
        is given
        """
        # render each of them
        return self._fieldList(query=query, spec=query.group, parameters=parameters)

    def _orderClause(self, query, parameters=None):
        """
        Render the order of the rows of {query}, whose values go to {parameters}, when it is
        given
        """
        # render each of its collations
        return self._fieldList(query=query, spec=query.order, parameters=parameters)

    def _fieldList(self, query, spec, parameters=None):
        """
        Render {spec}, one expression or several, in the context of {query}; its values go to
        {parameters}, when it is given
        """
        # a single expression
        if not isinstance(spec, collections.abc.Iterable):
            # is a list of one
            spec = (spec,)
        # render each one, separated by commas
        return ", ".join(
            self.expression(root=entry, context=query, parameters=parameters) for entry in spec
        )

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

    def savepoint(self, name):
        """
        Generate the SQL statement that marks the work done so far in a transaction with the
        savepoint {name}
        """
        # every statement starts at the margin
        self.margin()
        # simple enough
        yield self.place(f"SAVEPOINT {self.identifier(name)};")
        # all done
        return

    def releaseSavepoint(self, name):
        """
        Generate the SQL statement that keeps the work done since the savepoint {name}, and
        forgets the savepoint
        """
        # every statement starts at the margin
        self.margin()
        # simple enough
        yield self.place(f"RELEASE SAVEPOINT {self.identifier(name)};")
        # all done
        return

    def rollbackToSavepoint(self, name):
        """
        Generate the SQL statement that undoes the work done since the savepoint {name}
        """
        # every statement starts at the margin
        self.margin()
        # simple enough
        yield self.place(f"ROLLBACK TO SAVEPOINT {self.identifier(name)};")
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
    def createTable(self, table, existOk=False, indexes=True, selfReferences=True):
        """
        Generate the SQL statement to create a database table given its description, followed
        by those that create its indexes unless {indexes} is off; with {existOk}, finding the
        table and its indexes there already is fine; without {selfReferences}, the references of
        the table to itself are left for {addSelfReferences}, in a language that can add them

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
        # and the declarations that follow the columns, with the references of the table to itself
        # unless they are to be added later, which a language that cannot add them never does
        annotations = tuple(
            self._tableAnnotations(
                table=table, selfReferences=selfReferences or not self.addsReferences
            )
        )
        # the statements that record the documentation of the table in the catalog of the server
        notes = tuple(self._documentation(table=table))
        # and those that create its indexes, when they are wanted
        followers = tuple(self.createIndexes(table=table, existOk=existOk)) if indexes else ()
        # and the opening of the statement, which says whether the table may exist already
        header = (
            "CREATE TABLE"
            + self._ifMissing(existOk=existOk, subject=f"the table {table.pyre_name}")
            + f" {self.identifier(table.pyre_name)}"
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

    def _tableAnnotations(self, table, selfReferences=True):
        """
        Generate the declarations that follow the columns of {table}: its keys, its references to
        other tables, and to itself unless {selfReferences} is off, and its checks
        """
        # the primary key, if there is one
        if table._pyre_primaryKeys:
            # the names of its fields, in order
            names = ",".join(self.identifier(field.name) for field in table._pyre_primaryKeys)
            # make up the declaration
            yield f"PRIMARY KEY ({names})"
        # each group of fields whose values are unique together
        for fields, name in table._pyre_uniqueKeys:
            # is a constraint of its own
            yield self._constraint(
                name=name,
                rule=f"UNIQUE ({','.join(self.identifier(field.name) for field in fields)})",
            )
        # each reference to a table, this one among them
        for local, foreign, name in table._pyre_foreignKeys:
            # a reference to the table itself, when it is to be added later
            if foreign.table is table and not selfReferences:
                # is left for then
                continue
            # the others name the field, the table, and the field of the other table
            yield self._constraint(name=name, rule=self._foreignKey(local=local, foreign=foreign))
        # and each check
        for constraint, name in table._pyre_constraints:
            # renders its expression in the context of the table
            yield self._constraint(
                name=name, rule=f"CHECK ({self.expression(root=constraint, context=table)})"
            )
        # all done
        return

    def addSelfReferences(self, table):
        """
        Generate the statements that add the references of {table} to itself, which a table made
        without them gets once its rows are in; a language that cannot add them declared them
        with the table, and has nothing to add
        """
        # a language that cannot add a reference to a table that exists
        if not self.addsReferences:
            # declared them already
            return
        # go through the references of the table
        for local, foreign, name in table._pyre_foreignKeys:
            # the ones to other tables were declared with it
            if foreign.table is not table:
                # so move on
                continue
            # every statement starts at the margin
            self.margin()
            # add each of the others in a statement of its own
            yield self.place(
                f"ALTER TABLE {self.identifier(table.pyre_name)} ADD "
                + self._constraint(name=name, rule=self._foreignKey(local=local, foreign=foreign))
                + ";"
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
        yield self.place(f"DROP TABLE{clause} {self.identifier(table.pyre_name)};")
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
        yield self.place(f"DROP INDEX{clause} {self.identifier(name)};")
        # all done
        return

    def restartIdentity(self, table, field, start):
        """
        Generate the SQL statement that makes the server assign the values of {field}, a column of
        {table} whose values it assigns, from {start} on
        """
        # every statement starts at the margin
        self.margin()
        # the table and the column
        target = f"{self.identifier(table.pyre_name)} ALTER COLUMN {self.identifier(field.name)}"
        # build the statement
        yield self.place(f"ALTER TABLE {target} RESTART WITH {int(start)};")
        # all done
        return

    # record management
    def insertRecords(
        self, *records, returning=None, existing=None, key=None, parameters=None, generated=None
    ):
        """
        Insert {records}, an iterable of table records, into their corresponding table; the
        consecutive records of a table that name the same columns share a statement; each
        statement returns the columns of {returning}, a table or a query, when it is given

        With {existing}, a row whose {key} matches one that is there already is either left
        alone, when {existing} is "keep", or written over it, when it is "replace"; the key is
        the primary key of the table, unless {key} names the fields of another

        A value for a column whose values the server assigns, and takes from no row, is refused,
        unless {generated} is "keep", which has the server take it over its own
        """
        # go through the statements
        for statement in self.insertStatements(
            *records,
            returning=returning,
            existing=existing,
            key=key,
            parameters=parameters,
            generated=generated,
        ):
            # and hand over their lines
            yield from statement
        # all done
        return

    def insertStatements(
        self, *records, returning=None, existing=None, key=None, parameters=None, generated=None
    ):
        """
        Generate the statements that insert {records}, as {insertRecords} describes them, each
        one whole, as a tuple of its lines; with {parameters}, the values of each statement are
        kept there by the time the statement is handed over, and placeholders take their place
        """
        # the clause that returns the rows, built before anything is rendered
        clause = None if returning is None else self._returning(returning=returning)
        # a request about the rows that are there already
        if existing is not None and existing not in self.existingRows:
            # that is neither of the two is a mistake in the code that made it
            import journal

            # so complain
            raise journal.firewall("pyre.db").log(
                f"existing rows may be kept or replaced, not {existing!r}"
            )
        # make sure the request about the values of the columns the server assigns is one the
        # language knows
        self._generatedRequest(generated=generated)
        # a language whose inserts cannot meet the rows that are there already
        if existing is not None and not self.hasConflict:
            # merges the records instead
            yield from self._merge(
                records=records,
                existing=existing,
                key=key,
                parameters=parameters,
                generated=generated,
            )
            # and that's all
            return
        # every statement starts at the margin
        self.margin()
        # the lines of the statement in progress
        lines = []
        # the values of the previous record, held back until we know whether more follow, so
        # that {records} can be a generator
        dangling = ""
        # the shape of the statement in progress, if any: its table and its columns
        shape = None
        # and whether it says that it keeps the values its rows bring for the columns the server
        # assigns
        overrides = False
        # iterate over the records
        for record in records:
            # get the table of the record
            table = record.pyre_layout
            # the columns it names, with their values
            columns = tuple(self._insertColumns(table=table, record=record))
            # and its shape
            recordShape = (table, tuple(field.name for field, _ in columns))
            # whether it must say that it keeps the values it brings for the columns the server
            # assigns
            overriding = self._overriding(table=table, columns=columns, generated=generated)
            # a record of the same shape as the statement in progress, that overrides as it does
            if recordShape == shape and overriding == overrides:
                # joins it, so render the dangling values, followed by a comma
                lines.append(self.place(dangling + ","))
            # the others
            else:
                # end the statement in progress, if there is one
                if shape is not None:
                    # by terminating it
                    lines.extend(
                        self._insertEnd(
                            values=dangling,
                            tail=self._insertTail(
                                shape=shape, existing=existing, key=key, clause=clause
                            ),
                        )
                    )
                    # bouncing out to the margin
                    self.outdent(decrement=2)
                    # and handing it over
                    yield tuple(lines)
                    # before starting the next one
                    lines = []
                # a record that names no column
                if not columns:
                    # is inserted by a statement of its own, which returns its row when asked
                    yield (
                        self.place(
                            f"INSERT INTO {self.identifier(table.pyre_name)} DEFAULT VALUES"
                            + ("" if clause is None else f" {clause}")
                            + ";"
                        ),
                    )
                    # which leaves no statement in progress
                    shape = None
                    # so move on
                    continue
                # the others start a statement of their shape
                shape = recordShape
                # that overrides as they do
                overrides = overriding
                # initiate it
                lines.append(self.place(f"INSERT INTO {self.identifier(table.pyre_name)}"))
                # indent
                self.indent(increment=2)
                # the names of the columns
                lines.append(
                    self.place(
                        "(" + ", ".join(self.identifier(name) for name in recordShape[1]) + ")"
                    )
                )
                # push out
                self.outdent()
                # a statement whose rows bring values for the columns the server assigns
                if overrides:
                    # has them taken over the server's own
                    lines.append(self.place("OVERRIDING SYSTEM VALUE"))
                # start the section with the record values
                lines.append(self.place("VALUES"))
                # further in
                self.indent()
            # collect the values
            values = (
                self._recordValue(table=table, field=field, value=value, parameters=parameters)
                for field, value in columns
            )
            # render them
            dangling = "(" + ", ".join(values) + ")"

        # if there is no statement in progress
        if shape is None:
            # there is nothing left to render
            return
        # render any left overs
        lines.extend(
            self._insertEnd(
                values=dangling,
                tail=self._insertTail(shape=shape, existing=existing, key=key, clause=clause),
            )
        )
        # bounce out to top level
        self.outdent(decrement=2)
        # and hand the last statement over
        yield tuple(lines)
        # all done
        return

    def loadGroups(self, *records, generated=None):
        """
        Sort {records} by their table and by the columns they give values for, and generate each
        group as its table, the fields of those columns and its records, in the order in which
        the groups first appear; a value for a column whose values the server assigns, and takes
        from no row, is refused, unless {generated} is "keep"
        """
        # make sure the request about the values of the columns the server assigns is one the
        # language knows
        self._generatedRequest(generated=generated)
        # the groups, by their table and the names of their columns
        groups = {}
        # go through the records
        for record in records:
            # get the table of the record
            table = record.pyre_layout
            # the columns it gives values for, with their values
            columns = tuple(self._givenColumns(table=table, record=record))
            # which may bring values for the columns the server assigns only when they are kept;
            # the loaders take them without being told
            self._overriding(table=table, columns=columns, generated=generated)
            # the fields it gives values for
            fields = tuple(field for field, _ in columns)
            # the group of the records of its table that give values for the same fields
            group = groups.setdefault(
                (table, tuple(field.name for field in fields)), (table, fields, [])
            )
            # takes it
            group[2].append(record)
        # hand the groups over
        yield from groups.values()
        # all done
        return

    def givenValues(self, table, record):
        """
        Build the values {record} gives the columns of {table} it does not leave to the server,
        in the order of the fields {loadGroups} reports for it
        """
        # easy enough
        return tuple(value for _, value in self._givenColumns(table=table, record=record))

    def loadStatement(self, table, fields, parameters):
        """
        Build the statement that inserts a row of {table} with a value for each of {fields}, each
        one a placeholder spelled by {parameters}, so that the statement serves every row of a
        group
        """
        # the names of the columns
        names = ", ".join(self.identifier(field.name) for field in fields)
        # and the placeholders of their values
        marks = ", ".join(parameters.placeholders(count=len(fields)))
        # put it all together
        return f"INSERT INTO {self.identifier(table.pyre_name)} ({names}) VALUES ({marks});"

    def deleteRecords(self, table, condition, returning=None, parameters=None):
        """
        Remove all {table} records that match {condition}, and return the columns of
        {returning}, a table or a query, when it is given; with {parameters}, the values in the
        statement are kept there, and placeholders take their place

        If condition is {None}, this routine will remove all records from the given {table}
        """
        # the clause that returns the rows, built before anything is rendered
        clause = None if returning is None else self._returning(returning=returning)
        # every statement starts at the margin
        self.margin()
        # the lines of the statement: the table
        lines = [self.place(f"DELETE FROM {self.identifier(table.pyre_name)}")]
        # indent
        self.indent()
        # if a condition was specified
        if condition is not None:
            # build the filtering expression
            predicate = self.expression(root=condition, context=table, parameters=parameters)
            # and render it
            lines.append(self.place(f"WHERE ({predicate})"))
        # if the rows are wanted back
        if clause is not None:
            # ask for them
            lines.append(self.place(clause))
        # outdent
        self.outdent()
        # end the statement
        lines[-1] += ";"
        # and hand it over
        yield from lines
        # all done
        return

    def updateRecords(self, template, condition, returning=None, parameters=None):
        """
        Update all table rows that match {condition} using information from {template}, a
        prototype row of a table. The update operation sets the fields in these rows to their
        corresponding values in {template}; fields set to {None} in {template} are not
        affected. Without a {condition}, every row is updated, and a {template} that sets no
        field builds no statement. The statement returns the columns of {returning}, a table or
        a query, when it is given; with {parameters}, the values in the statement are kept
        there, and placeholders take their place
        """
        # the clause that returns the rows, built before anything is rendered
        clause = None if returning is None else self._returning(returning=returning)
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
            rendered = self._recordValue(
                table=table, field=field, value=value, parameters=parameters
            )
            # by name
            assignments.append(f"{self.identifier(field.name)} = {rendered}")
        # if there is nothing to set
        if not assignments:
            # there is no statement
            return
        # the lines of the statement: the table
        lines = [self.place(f"UPDATE {self.identifier(table.pyre_name)}")]
        # indent
        self.indent()
        # the data section
        lines.append(self.place("SET"))
        # indent
        self.indent()
        # render the assignments, each but the last followed by a comma
        for index, assignment in enumerate(assignments):
            # place it
            lines.append(self.place(assignment + ("," if index + 1 < len(assignments) else "")))
        # outdent
        self.outdent()
        # if there is a restriction
        if condition is not None:
            # build the filtering expression
            predicate = self.expression(root=condition, context=table, parameters=parameters)
            # and render it
            lines.append(self.place(f"WHERE ({predicate})"))
        # if the rows are wanted back
        if clause is not None:
            # ask for them
            lines.append(self.place(clause))
        # outdent
        self.outdent()
        # end the statement
        lines[-1] += ";"
        # and hand it over
        yield from lines
        # all done
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
            return self.identifier(node.table.pyre_name)
        # a field of no table in particular, or of the table in context or one of its bases
        if not node.table or (isinstance(context, type) and issubclass(context, node.table)):
            # is named by itself
            return self.identifier(node.field.name)
        # any other is qualified by the name of its table
        return f"{self.identifier(node.table.pyre_name)}.{self.identifier(node.field.name)}"

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

    def _pyre_onIsIn(self, node, parameters=None, **kwds):
        """
        Render {node}, the test of whether a field holds one of a list of values, or one of the
        rows of a query; with {parameters}, the values are kept there, and placeholders take
        their place
        """
        # render the field
        field = self.expression(root=node.field, parameters=parameters, **kwds)
        # values drawn from the rows of a query
        if isinstance(node.values, self.selector):
            # come from its selection
            return f"{field} IN ({self._subquery(query=node.values, parameters=parameters)})"
        # the others are a list
        values = tuple(node.values)
        # no field holds one of no values, and the language has no empty list to say it with
        if not values:
            # so say what it means
            return "FALSE"
        # the values travel beside the statement when there is a place for them
        writer = self._literals if parameters is None else parameters
        # render them
        rendered = ", ".join(writer.value(value=value) for value in values)
        # and put it all together
        return f"{field} IN ({rendered})"

    def _pyre_onLike(self, node, parameters=None, **kwds):
        """
        Render {node}, the match of a field against a pattern, naming the character that escapes
        its wildcards, since the back ends disagree on what it is when it is left out; with
        {parameters}, the pattern and the escape character are kept there, and placeholders take
        their place
        """
        # render the field
        field = self.expression(root=node.field, parameters=parameters, **kwds)
        # the pattern and its escape character travel beside the statement when there is a place
        # for them
        if parameters is not None:
            # so keep the pattern
            pattern = parameters.value(value=node.pattern)
            # and the escape character
            escape = parameters.value(value=node.escape)
        # otherwise
        else:
            # quote the pattern
            pattern = self.quote(text=node.pattern)
            # and the escape character
            escape = self.quote(text=node.escape)
        # put it all together
        return f"({field} LIKE {pattern} ESCAPE {escape})"

    # names
    def identifier(self, name):
        """
        Render {name} as the language reads it: as it is, when it is made of lower case letters,
        digits and underscores, does not start with a digit, and is not a word the language
        reserves; quoted, with any double quotes in it doubled, otherwise
        """
        # a name the language reads as it is
        if self.plain.fullmatch(name) and name not in self.reserved:
            # stays as it is
            return name
        # the others are quoted
        return '"' + name.replace('"', '""') + '"'

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
        return f"CONSTRAINT {self.identifier(name)} {rule}"

    def _foreignKey(self, local, foreign):
        """
        Build the rule of the reference of the field {local} to the field {foreign} of a table
        """
        # name the field, the table, and the field of the table it refers to
        return (
            f"FOREIGN KEY ({self.identifier(local.field.name)}) "
            f"REFERENCES {self.identifier(foreign.table.pyre_name)}"
            f" ({self.identifier(foreign.field.name)})"
        )

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
        fields = ", ".join(self.identifier(field.name) for field in index.fields)
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
            f"CREATE {unique}INDEX{clause} {self.identifier(name)}"
            f" ON {self.identifier(table.pyre_name)} ({fields}){where};"
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

    def _literalRenderer(self, node, parameters=None, **kwds):
        """
        Render {node}, a literal in an expression, whose value belongs to no column; with
        {parameters}, the value is kept there, and its placeholder takes its place
        """
        # the value travels beside the statement when there is a place for it
        writer = self._literals if parameters is None else parameters
        # a slot of a prepared statement
        if isinstance(node._value, Parameter):
            # stands for a value that is given when the statement runs
            return writer.valueSlot(parameter=node._value)
        # the rendering of the others depends only on their type
        return writer.value(value=node._value)

    def _insertColumns(self, table, record):
        """
        Generate the columns of {table} that {record} names in an insert, with their values
        """
        # every column, in declaration order
        yield from zip(table.pyre_fields, record)
        # all done
        return

    def _recordValue(self, table, field, value, parameters=None):
        """
        Render {value}, the value of {field} in a record of {table}, for an insert or an update;
        with {parameters}, the value is kept there, and its placeholder takes its place
        """
        # a missing value
        if value is None:
            # is left to the server in a column whose values it assigns, and is {NULL} elsewhere
            return "DEFAULT" if field._autogenerated else "NULL"
        # the special values {DEFAULT} and {NULL}
        if value is table.default or value is table.null:
            # render as themselves
            return value.value
        # everything else is a value of its column, which travels beside the statement when
        # there is a place for it, and is a literal otherwise
        writer = self._literals if parameters is None else parameters
        # a slot of a prepared statement
        if isinstance(value, Parameter):
            # stands for a value of its column that is given when the statement runs
            return writer.slot(table=table, column=field, parameter=value)
        # the others are rendered as they are
        return writer.literal(table=table, column=field, value=value)

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
        name = self.identifier(field.name)
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
            yield self.place(f"REFERENCES {self.identifier(table.pyre_name)}{separator}")
        # otherwise
        else:
            # name the table and the field
            yield self.place(
                f"REFERENCES {self.identifier(table.pyre_name)}"
                f" ({self.identifier(field.name)}){separator}"
            )

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
