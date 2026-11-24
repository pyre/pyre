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

# the statements that are rendered once and run many times
from .Prepared import Prepared


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
    # the generator of my statements
    sql = pyre.weaver.language(default=Mill)
    sql.doc = "the generator of the SQL statements"

    # how many rows a selection reads at a time, when the back end hands them over as it reads
    batch = pyre.properties.int()
    batch.default = 1000
    batch.validators = pyre.constraints.isPositive()
    batch.doc = "the number of rows a selection fetches from the back end at a time"

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

    def run(self, statement, *arguments):
        """
        Execute a single {statement}, with its placeholders filled in by {arguments}, which
        travel beside it
        """
        # running is the job of the back end specific subclasses that take parameters
        raise NotImplementedError(f"class '{type(self).__name__}' must override 'run'")

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

    def insert(self, *records, returning=None, existing=None, key=None, generated=None):
        """
        Insert {records} into the database; with {returning}, a table, one of its fields or a
        sequence of them, hand back the rows the inserts add, as records

        With {existing}, a record whose {key} matches a row that is there already leaves it
        alone, when {existing} is "keep", or writes over it, when it is "replace"; the key is
        the primary key of the table, unless {key} names the fields of another

        A value for a column whose values the server assigns, and takes from no row, is refused,
        unless {generated} is "keep", which has the server take it over its own
        """
        # if there are no records to insert, bail
        if not records:
            # with nothing to show for it
            return None if returning is None else []
        # the place for the values of the statements, if they travel beside them
        parameters = self._parameters()
        # without rows to hand back
        if returning is None:
            # build the statements
            sql = self.sql.insertStatements(
                *records, existing=existing, key=key, parameters=parameters, generated=generated
            )
            # and execute them
            return self._runAll(statements=sql, parameters=parameters)
        # otherwise, build the selection of the rows the inserts add
        selection = self._returned(
            returning=returning, tables={record.pyre_layout for record in records}
        )
        # build the statements
        sql = self.sql.insertStatements(
            *records,
            returning=selection,
            existing=existing,
            key=key,
            parameters=parameters,
            generated=generated,
        )
        # and run them, gathering their rows
        return self._gather(statements=sql, selection=selection, parameters=parameters)

    def load(self, *records, generated=None):
        """
        Insert {records}, many at a time and all or nothing; the records of a table that give
        values for the same columns travel together

        A load hands back no rows, and refuses a record whose key is there already; {insert}
        offers both. It refuses a value for a column whose values the server assigns, and takes
        from no row, unless {generated} is "keep", as {insert} does
        """
        # in a block of its own, so that the load keeps all of its records or none of them
        with self:
            # the standard way to put records in a table is to insert them
            self.insert(*records, generated=generated)
        # all done
        return self

    def reproduce(self, *, source, tables):
        """
        Make {tables} in my database, with the rows, the keys and the indexes they have in the
        database of {source}; a table comes before the tables that refer to it, and all of them
        appear together or not at all

        Each table is made without its indexes, filled {batch} rows at a time with the values its
        rows have, the ones {source} assigned among them, given its indexes, and told to assign
        the values of its generated columns after the largest it was given
        """
        # put the tables in an order that lets each find the rows it refers to
        ordered = self._dependencyOrder(tables=tables)
        # in a block of its own, so that the tables appear together or not at all
        with self:
            # go through them
            for table in ordered:
                # and reproduce each one
                self._reproduceTable(source=source, table=table)
        # all done
        return self

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
        # the place for the values of the statements, if they travel beside them
        parameters = self._parameters()
        # the statements, one for each specification that sets something
        statements = (
            self.sql.updateRecords(
                template=template, condition=condition, returning=selection, parameters=parameters
            )
            for template, condition in specifications
        )
        # each one whole, with its values
        pairs = [
            (lines, values)
            for lines, values in self._paired(
                statements=(tuple(sql) for sql in statements), parameters=parameters
            )
            if lines
        ]
        # without rows to hand back
        if selection is None:
            # several statements are all or nothing
            with self if len(pairs) > 1 else contextlib.nullcontext():
                # go through them
                for lines, values in pairs:
                    # and execute each one
                    self._run(lines=lines, values=values, parameters=parameters)
            # all done
            return None
        # otherwise, run them, gathering their rows
        return self._gatherPairs(pairs=pairs, selection=selection, parameters=parameters)

    def delete(self, table, condition, returning=None):
        """
        Delete all {table} records that match {condition}; with {returning}, the table, one of
        its fields or a sequence of them, hand back the rows the deletion removes, as records
        """
        # the place for the values of the statement, if they travel beside it
        parameters = self._parameters()
        # the selection of the rows the deletion removes, when they are wanted back
        selection = (
            None if returning is None else self._returned(returning=returning, tables={table})
        )
        # build the statement
        sql = self.sql.deleteRecords(
            table=table, condition=condition, returning=selection, parameters=parameters
        )
        # without rows to hand back
        if selection is None:
            # execute it
            return self._runAll(statements=(tuple(sql),), parameters=parameters)
        # otherwise, run it, gathering its rows
        return self._gather(statements=(tuple(sql),), selection=selection, parameters=parameters)

    def restartIdentity(self, table, field, start):
        """
        Make the server assign the values of {field}, a column of {table} whose values it
        assigns, from {start} on
        """
        # build the statement; a language that has nothing to say about it builds none
        statement = tuple(self.sql.restartIdentity(table=table, field=field, start=start))
        # so run the one that is there
        if statement:
            # and only that
            self.execute(*statement)
        # all done
        return self

    def lock(self, name, wait=True, timeout=None):
        """
        Hold the lock {name} from the start of a block to its end; a back end without locks of
        the application's own refuses it
        """
        # say so
        raise self.exceptions.NotSupportedError(
            diagnostic=f"{self.sql.dialect} has no advisory locks"
        )

    def select(self, query, limit=None, offset=None):
        """
        Execute the given {query} and generate the records of the rows it retrieves, as the back
        end hands them over; {offset} skips that many of the first rows, and {limit} keeps at
        most that many of the rest
        """
        # the place for the values of the statement, if they travel beside it
        parameters = self._parameters()
        # build the statement
        sql = tuple(self.sql.select(query=query, limit=limit, offset=offset, parameters=parameters))
        # and pair it with its values
        ((lines, values),) = self._paired(statements=(sql,), parameters=parameters)

        # walk the rows the back end hands over, which are data rows and nothing else, as records
        yield from self._records(
            rows=self._fetch(lines=lines, values=values, parameters=parameters), selection=query
        )
        # all done
        return

    # prepared statements
    def prepareSelect(self, query, limit=None, offset=None):
        """
        Prepare the selection {select} makes of {query}, with its bounds {limit} and {offset};
        the slots in its restriction and its bounds are filled in at each run, which hands back
        the rows one at a time
        """

        # the recipe of the statement
        def build(parameters):
            """
            Write the selection into {parameters}
            """
            # as {select} does
            return self.sql.select(query=query, limit=limit, offset=offset, parameters=parameters)

        # make one
        return Prepared(server=self, build=build, selection=query, stream=True)

    def prepareUpdate(self, template, condition, returning=None):
        """
        Prepare the update {update} makes of the rows that match {condition} with the values of
        {template}; the slots in either are filled in at each run, which hands back the rows the
        update changes, as records, with {returning}, and nothing otherwise
        """
        # the selection of the rows the update changes, when they are wanted back
        selection = (
            None
            if returning is None
            else self._returned(returning=returning, tables={template.pyre_layout})
        )

        # the recipe of the statement
        def build(parameters):
            """
            Write the update into {parameters}
            """
            # as {update} does
            return self.sql.updateRecords(
                template=template, condition=condition, returning=selection, parameters=parameters
            )

        # make one
        return Prepared(server=self, build=build, selection=selection)

    def prepareDelete(self, table, condition, returning=None):
        """
        Prepare the deletion {delete} makes of the rows of {table} that match {condition}; the
        slots in the condition are filled in at each run, which hands back the rows the deletion
        removes, as records, with {returning}, and nothing otherwise
        """
        # the selection of the rows the deletion removes, when they are wanted back
        selection = (
            None if returning is None else self._returned(returning=returning, tables={table})
        )

        # the recipe of the statement
        def build(parameters):
            """
            Write the deletion into {parameters}
            """
            # as {delete} does
            return self.sql.deleteRecords(
                table=table, condition=condition, returning=selection, parameters=parameters
            )

        # make one
        return Prepared(server=self, build=build, selection=selection)

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

    def _parameters(self):
        """
        Make a place for the values of a statement, which travel beside it; a server that writes
        them into its statements as literals has none
        """
        # i write literals
        return None

    def _paired(self, statements, parameters):
        """
        Pair each of {statements}, each a tuple of its lines, with the values {parameters} kept
        while it was built, or with none when there is no place for them
        """
        # the pairs
        pairs = []
        # go through the statements, each of which is whole when it arrives
        for lines in statements:
            # a statement with slots
            if parameters is not None:
                # has values only once it is prepared
                self._refuseSlots(parameters=parameters)
            # take its values before the next one is built
            pairs.append((lines, () if parameters is None else parameters.drain()))
        # hand them over
        return pairs

    def _refuseSlots(self, parameters):
        """
        Refuse a statement whose {parameters} kept slots, which have values only when a prepared
        statement runs
        """
        # the names of the slots
        names = [name for name, _ in parameters.slots()]
        # a statement with none
        if not names:
            # is fine
            return
        # the others are a mistake of the caller
        raise self.exceptions.InterfaceError(
            diagnostic=(
                f"no values for the slots {', '.join(map(repr, names))}: a statement with slots "
                f"runs once it is prepared"
            )
        )

    def _records(self, rows, selection):
        """
        Generate the records of {selection} that {rows}, as the back end sent them, hold
        """
        # the columns of the selection, one for each field
        columns = selection.pyre_fields
        # go through the rows
        for row in rows:
            # turn each value into the type of its column
            values = (
                self.interpret(column=column, value=value, selection=selection)
                for column, value in zip(columns, row)
            )
            # and build the record out of them
            yield selection.pyre_storedTuple(record=selection, data=values)
        # all done
        return

    def _runPrepared(self, prepared, values, arguments):
        """
        Run the statement of {prepared}, with its slots filled in from {values}, and hand back
        the rows the back end sent; a server that writes its values as literals writes the
        statement anew, with the literals of {values}, and ignores the bound {arguments}
        """
        # make a writer of literals that knows the values of the slots
        literals = self.sql.literals(mill=self.sql, values=values)
        # write the statement with it, and execute it
        return self.execute(*prepared.build(literals))

    def _releasePrepared(self, prepared):
        """
        Release what the back end keeps on behalf of {prepared}; a server that writes its values
        as literals keeps nothing there
        """
        # so there is nothing to do
        return self

    def _run(self, lines, values, parameters):
        """
        Execute the statement whose lines are {lines}, with its {values} beside it when there is
        a place for them
        """
        # a statement whose values are literals
        if parameters is None:
            # is executed as it is
            return self.execute(*lines)
        # the others are run with their values
        return self.run("\n".join(lines), *values)

    def _fetch(self, lines, values, parameters):
        """
        Run the selection whose lines are {lines}, with its {values} beside it when there is a
        place for them, and hand back its rows; a back end that hands them over as they are
        read fetches {batch} of them at a time
        """
        # the standard way is to run the statement, which hands back all of its rows at once
        return self._run(lines=lines, values=values, parameters=parameters)

    def _runAll(self, statements, parameters):
        """
        Execute {statements}, each a tuple of its lines, all or nothing, and hand back the result
        of the last one
        """
        # statements whose values are literals
        if parameters is None:
            # go to the back end as a single command, which is all or nothing on its own
            return self.execute(*(line for lines in statements for line in lines))
        # the others are paired with their values
        pairs = self._paired(statements=statements, parameters=parameters)
        # the result of the last one
        result = None
        # several statements are all or nothing
        with self if len(pairs) > 1 else contextlib.nullcontext():
            # go through them
            for lines, values in pairs:
                # and run each one
                result = self._run(lines=lines, values=values, parameters=parameters)
        # all done
        return result

    def _gather(self, statements, selection, parameters):
        """
        Run {statements}, each a tuple of its lines, one at a time, and gather the rows they
        hand back as records of {selection}
        """
        # pair them with their values
        pairs = self._paired(statements=statements, parameters=parameters)
        # and run them
        return self._gatherPairs(pairs=pairs, selection=selection, parameters=parameters)

    def _gatherPairs(self, pairs, selection, parameters):
        """
        Run the statements in {pairs}, each a tuple of its lines and its values, one at a time,
        and gather the rows they hand back as records of {selection}
        """
        # the rows
        rows = []
        # several statements are all or nothing
        with self if len(pairs) > 1 else contextlib.nullcontext():
            # run each statement
            for lines, values in pairs:
                # and keep the records of the rows it hands back
                rows.extend(
                    self._records(
                        rows=self._run(lines=lines, values=values, parameters=parameters),
                        selection=selection,
                    )
                )
        # hand the rows over
        return rows

    def _dependencyOrder(self, tables):
        """
        Put {tables} in an order in which each comes after the ones among them it refers to; the
        tables it refers to that are not among them are not mine to place, and tables that refer
        to each other in a cycle are refused
        """
        # the tables to place, in the order they were given
        pending = list(tables)
        # the order
        ordered = []
        # until every table is placed
        while pending:
            # the tables whose references among the ones to place are all placed
            ready = [
                table
                for table in pending
                if all(
                    other in ordered or other not in pending
                    for other in table.pyre_referencedTables()
                )
            ]
            # if there are none, the rest refer to each other
            if not ready:
                # so no order lets each of them find the rows it refers to
                raise self.exceptions.NotSupportedError(
                    diagnostic=(
                        f"the tables {', '.join(table.pyre_name for table in pending)} refer to"
                        " each other, so none of them can be made before the others"
                    )
                )
            # place the ones that are ready, in the order they were given
            ordered.extend(ready)
            # and look again at the rest
            pending = [table for table in pending if table not in ready]
        # hand the order over
        return ordered

    def _reproduceTable(self, source, table):
        """
        Make {table} in my database with the rows, the keys and the indexes it has in the database
        of {source}
        """
        # make the table, without its indexes, which are cheaper to build once the rows are in
        self.createTable(table, indexes=False)
        # the columns whose values the server assigns
        generated = [field for field in table.pyre_fields if field._autogenerated]
        # and the largest value of each among the rows, by the name of the column
        largest = {field.name: None for field in generated}
        # the rows read but not yet written
        rows = []
        # go through the rows of the table
        for row in source.select(query=table):
            # note the values of its generated columns
            for field in generated:
                # one at a time
                value = getattr(row, field.name)
                # when it is the largest so far
                if value is not None and (
                    largest[field.name] is None or value > largest[field.name]
                ):
                    # keep it
                    largest[field.name] = value
            # hold on to the row
            rows.append(row)
            # and once there are enough of them
            if len(rows) >= self.batch:
                # write them, with the values the source assigned
                self.load(*rows, generated="keep")
                # and start over
                rows = []
        # write the rows that are left
        if rows:
            # with the values the source assigned
            self.load(*rows, generated="keep")
        # build the indexes, now that the rows are in
        self.createIndexes(table)
        # go through the generated columns
        for field in generated:
            # a column without values
            if largest[field.name] is None:
                # starts where it would have anyway
                continue
            # the others start after their largest value
            self.restartIdentity(table=table, field=field, start=largest[field.name] + 1)
        # all done
        return

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
