# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import contextlib
import types

# packages
import pyre

# the protocol i implement
from .DataStore import DataStore

# and the mill that speaks standard SQL, which is the default of every server
from .backends.standard.Mill import Mill

# the references to the fields of tables
from .schema.FieldReference import FieldReference

# and the base of queries, for those over the rows a statement hands back
from .queries.Query import Query


# declaration
class Server(pyre.component, implements=DataStore):
    """
    Abstract component that encapsulates the connection to a database back end

    This class is meant to be used as the base class for back end specific component
    implementations. It builds every statement of the {DataStore} interface out of the SQL
    generator, and leaves {attach}, {detach} and {execute} to the back ends
    """

    # types
    # exceptions
    from . import exceptions

    # traits
    sql = pyre.weaver.language(default=Mill)
    sql.doc = "the generator of the SQL statements"

    # required interface
    @pyre.export
    def attach(self):
        """
        Connect to the database back end
        """
        # connecting is the job of the back end specific subclasses
        raise NotImplementedError(f"class '{type(self).__name__}' must override 'attach'")

    @pyre.export
    def detach(self):
        """
        Disconnect from the database back end
        """
        # disconnecting is the job of the back end specific subclasses
        raise NotImplementedError(f"class '{type(self).__name__}' must override 'detach'")

    @pyre.export
    def execute(self, *sql):
        """
        Execute the sequence of SQL statements in {sql} as a single command
        """
        # executing is the job of the back end specific subclasses
        raise NotImplementedError(f"class '{type(self).__name__}' must override 'execute'")

    # convenience
    def createDatabase(self, name, existOk=False):
        """
        Build and execute the SQL statement to create the database {name}; with {existOk},
        finding it there already is fine
        """
        # build the sql statement
        sql = self.sql.createDatabase(name=name, existOk=existOk)
        # and execute it
        return self.execute(*sql)

    def dropDatabase(self, name, missingOk=False):
        """
        Build and execute the SQL statement to drop the database {name}; with {missingOk},
        finding it gone already is fine
        """
        # build the sql statement
        sql = self.sql.dropDatabase(name=name, missingOk=missingOk)
        # and execute it
        return self.execute(*sql)

    def createTable(self, table, existOk=False, indexes=True):
        """
        Build and execute the SQL statements necessary to create {table}, and its indexes unless
        {indexes} is off; with {existOk}, finding them there already is fine
        """
        # build the sql statements
        sql = self.sql.createTable(table=table, existOk=existOk, indexes=indexes)
        # and execute them
        return self.execute(*sql)

    def createIndexes(self, table, existOk=False):
        """
        Build and execute the SQL statements that create the indexes of {table}; with {existOk},
        finding them there already is fine
        """
        # build the sql statements
        sql = self.sql.createIndexes(table=table, existOk=existOk)
        # and execute them
        return self.execute(*sql)

    def createIndex(self, table, name, existOk=False):
        """
        Build and execute the SQL statement that creates the index {name} of {table}; with
        {existOk}, finding it there already is fine
        """
        # build the sql statement
        sql = self.sql.createIndex(table=table, name=name, existOk=existOk)
        # and execute it
        return self.execute(*sql)

    def dropIndex(self, table, name, missingOk=False):
        """
        Build and execute the SQL statement that drops the index {name} of {table}; with
        {missingOk}, finding it gone already is fine
        """
        # build the sql statement
        sql = self.sql.dropIndex(table=table, name=name, missingOk=missingOk)
        # and execute it
        return self.execute(*sql)

    def dropTable(self, table, missingOk=False):
        """
        Build and execute the SQL statement necessary to delete {table} from the datastore; with
        {missingOk}, finding it gone already is fine
        """
        # build the sql statement
        sql = self.sql.dropTable(table=table, missingOk=missingOk)
        # and execute it
        return self.execute(*sql)

    def insert(self, *records, returning=None, existing=None, key=None):
        """
        Insert {records} into the database; with {returning}, a table, one of its fields or a
        sequence of them, hand back the rows the inserts add, as records

        With {existing}, a record whose {key} matches a row that is there already leaves it
        alone, when {existing} is "keep", or writes over it, when it is "replace"; the key is
        the primary key of the table, unless {key} names the fields of another
        """
        # if there are no records to insert, bail
        if not records:
            # with nothing to show for it
            return None if returning is None else []
        # without rows to hand back
        if returning is None:
            # build the sql statements
            sql = self.sql.insertRecords(*records, existing=existing, key=key)
            # and execute them
            return self.execute(*sql)
        # otherwise, build the selection of the rows the inserts add
        selection = self._returned(
            returning=returning, tables={record.pyre_layout for record in records}
        )
        # build the statements
        sql = self.sql.insertRecords(*records, returning=selection, existing=existing, key=key)
        # and run them, gathering their rows
        return self._gather(lines=sql, selection=selection)

    def update(self, *specifications, returning=None):
        """
        Use {specifications} to update the database; with {returning}, a table, one of its
        fields or a sequence of them, hand back the rows the updates change, as records

        Each item in {specifications} is a pair of a {template} and a {condition}. The
        {template} is an instance of a table row with all fields that require update having
        values that are not {None}. The {condition} is an expression that identifies the
        portion of the table that will be affected
        """
        # the selection of the rows the updates change, when they are wanted back
        selection = (
            None
            if returning is None
            else self._returned(
                returning=returning,
                tables={template.pyre_layout for template, _ in specifications},
            )
        )
        # the statements, one for each specification that sets something
        statements = [
            sql
            for template, condition in specifications
            if (
                sql := tuple(
                    self.sql.updateRecords(
                        template=template, condition=condition, returning=selection
                    )
                )
            )
        ]
        # the rows the updates hand back
        rows = []
        # several statements are all or nothing
        with self if len(statements) > 1 else contextlib.nullcontext():
            # go through them
            for sql in statements:
                # a statement whose rows are not wanted
                if selection is None:
                    # is just executed
                    self.execute(*sql)
                    # and that's all
                    continue
                # the others hand their rows back
                rows.extend(self._gather(lines=sql, selection=selection))
        # all done
        return None if returning is None else rows

    def delete(self, table, condition, returning=None):
        """
        Delete all {table} records that match {condition}; with {returning}, the table, one of
        its fields or a sequence of them, hand back the rows the deletion removes, as records
        """
        # without rows to hand back
        if returning is None:
            # build the sql statements
            sql = self.sql.deleteRecords(table=table, condition=condition)
            # and execute
            return self.execute(*sql)
        # otherwise, build the selection of the rows the deletion removes
        selection = self._returned(returning=returning, tables={table})
        # build the statement
        sql = self.sql.deleteRecords(table=table, condition=condition, returning=selection)
        # and run it, gathering its rows
        return self._gather(lines=sql, selection=selection)

    def select(self, query, limit=None, offset=None):
        """
        Execute the given {query} and return the retrieved data; {offset} skips that many of
        the first rows, and {limit} keeps at most that many of the rest
        """
        # build the sql statements
        sql = self.sql.select(query=query, limit=limit, offset=offset)

        # the columns of the selection, one for each field of the query
        columns = query.pyre_fields
        # walk the rows the back end sent, which are data rows and nothing else
        for row in self.execute(*sql):
            # turn each value into the type of its column
            values = (
                self.interpret(column=column, value=value, selection=query)
                for column, value in zip(columns, row)
            )
            # and build the row out of them, as they are
            yield query.pyre_storedTuple(record=query, data=values)

        # all done
        return

    # reading
    def interpret(self, column, value, selection):
        """
        Turn {value}, which the back end sent for {column} of {selection}, into the type of the
        column
        """
        # {NULL} is {None}, whatever the column
        if value is None:
            # so leave it alone
            return None
        # otherwise, let the column say what it is, and pass it along, so a handler that refuses
        # the value can name it
        return column._pyre_identify(
            authority=self, value=value, column=column, selection=selection
        )

    # the handlers of the columns, which take a value as it is, unless a back end sends it in
    # another form
    def _pyre_onSchema(self, schema, value, **kwds):
        """
        Take {value} as it is
        """
        # easy enough
        return value

    def _pyre_onFieldReference(self, node, value, **kwds):
        """
        Turn {value} into the type of the field {node} refers to
        """
        # the field knows what it is
        return node.field._pyre_identify(authority=self, value=value, **kwds)

    def _pyre_onCast(self, node, value, **kwds):
        """
        Turn {value} into the target type of the conversion {node}
        """
        # the target type knows what it is
        return node.targetType._pyre_identify(authority=self, value=value, **kwds)

    # implementation details
    def _returned(self, returning, tables):
        """
        Build the selection of the rows a statement on {tables} hands back: {returning} is a
        table, whose records are the rows, or one of its fields or a sequence of them, whose rows
        are the records of a query over them
        """
        # a whole table
        if isinstance(returning, self.sql.schemer):
            # is its own selection
            table, selection = returning, returning
        # anything else is fields
        else:
            # one field
            if isinstance(returning, FieldReference):
                # makes a sequence of one
                fields = (returning,)
            # and the rest are sequences already
            else:
                # so take them in their order
                fields = tuple(returning)
            # the tables of the fields
            owners = {field.table for field in fields}
            # must be one table
            (table,) = owners if len(owners) == 1 else (None,)
            # whose query over the fields is built once
            selection = self._returnedQuery(table=table, fields=fields) if table else None
        # the statements must change the rows of that table
        if table is None or any(not issubclass(target, table) for target in tables):
            # or the request is a mistake in the code that made it
            import journal

            # the tables of the rows
            targets = ", ".join(repr(target.pyre_name) for target in tables)
            # and the table of the fields
            owner = repr(table.pyre_name) if table else "several tables"
            # say what is wrong
            raise journal.firewall("pyre.db").log(
                f"the rows of {targets} cannot return the fields of {owner}"
            )
        # hand over the selection
        return selection

    def _returnedQuery(self, table, fields):
        """
        Build, once, the query over {fields} of {table} whose records hold the rows a statement
        hands back
        """
        # the key of the query: the table and the names of its fields
        key = (table, tuple(field.field.name for field in fields))
        # look it up
        query = self._returnedQueries.get(key)
        # if it was built already
        if query is not None:
            # hand it over
            return query

        # otherwise, the body of its declaration
        def declare(namespace):
            """
            Declare a field of the query for each field of the table that is returned
            """
            # the table, as the query sees it
            alias = namespace["row"]
            # go through the fields
            for field in fields:
                # and declare each one under its own name
                namespace[field.field.name] = getattr(alias, field.field.name)
            # all done
            return

        # build the query
        query = types.new_class(
            f"{table.pyre_name}_returned", (Query,), {"row": table}, exec_body=declare
        )
        # remember it
        self._returnedQueries[key] = query
        # and hand it over
        return query

    def _gather(self, lines, selection):
        """
        Run the statements in {lines} one at a time, and gather the rows they hand back as
        records of {selection}
        """
        # the statements, each a list of its lines
        statements = []
        # the lines of the statement in progress
        statement = []
        # go through the lines
        for line in lines:
            # add each one to the statement
            statement.append(line)
            # and at the line that ends it
            if line.endswith(";"):
                # put it aside
                statements.append(statement)
                # and start the next one
                statement = []
        # the rows
        rows = []
        # several statements are all or nothing
        with self if len(statements) > 1 else contextlib.nullcontext():
            # run each statement
            for statement in statements:
                # and go through the rows it hands back
                for row in self.execute(*statement):
                    # turn each value into the type of its column
                    values = (
                        self.interpret(column=column, value=value, selection=selection)
                        for column, value in zip(selection.pyre_fields, row)
                    )
                    # and build the record
                    rows.append(selection.pyre_storedTuple(record=selection, data=values))
        # hand the rows over
        return rows

    def _commit(self):
        """
        Make the work of the transaction of a transaction block permanent
        """
        # tell the back end
        self.execute(*self.sql.commit())
        # all done
        return

    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the blocks that are open, the innermost last, each with the name of its savepoint, or
        # {None} for the transaction itself
        self._blocks = []
        # the number of savepoints set so far, which names the next one
        self._savepoints = 0
        # all done
        return

    # context manager support
    def __enter__(self):
        """
        Hook invoked when the context manager is entered: the outermost block is a transaction,
        and a block inside it is a savepoint
        """
        # a block inside another
        if self._blocks:
            # gets the next savepoint
            self._savepoints += 1
            # under its own name
            name = f"pyre_{self._savepoints}"
            # set it
            self.execute(*self.sql.savepoint(name=name))
        # the outermost block
        else:
            # has no savepoint
            name = None
            # and begins the transaction
            self.execute(*self.sql.transaction())
        # now that the block is open, remember it
        self._blocks.append(name)
        # and hand me back to the caller
        return self

    def __exit__(self, exc_type, exc_instance, exc_traceback):
        """
        Hook invoked when the context manager's block exits: a block that ends normally keeps
        its work, and one that raises undoes it; the outermost block commits or rolls back the
        transaction, and the others release or roll back to their savepoints
        """
        # the block that is closing
        name = self._blocks.pop()
        # a block inside another
        if name is not None:
            # that raised
            if exc_type is not None:
                # undoes its work
                self.execute(*self.sql.rollbackToSavepoint(name=name))
            # and either way, its savepoint is no longer needed
            self.execute(*self.sql.releaseSavepoint(name=name))
        # the outermost block that ended normally
        elif exc_type is None:
            # commits the transaction
            self._commit()
        # and the one that raised
        else:
            # rolls it back
            self.execute(*self.sql.rollback())
        # and re-raise any exception that occurred in the block
        return False

    # private data
    # the queries over the rows statements hand back, by table and fields; shared by every
    # server, since they depend only on the tables
    _returnedQueries = {}


# end of file
