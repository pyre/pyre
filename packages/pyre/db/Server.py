# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# packages
import pyre

# the protocol i implement
from .DataStore import DataStore

# and the mill that speaks standard SQL, which is the default of every server
from .backends.standard.Mill import Mill


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

    def insert(self, *records):
        """
        Insert {records} into the database
        """
        # if there are no records to insert, bail
        if not records:
            # with nothing to show for it
            return
        # build the sql statements
        sql = self.sql.insertRecords(*records)
        # and execute
        return self.execute(*sql)

    def update(self, *specifications):
        """
        Use {specifications} to update the database

        Each item in {specifications} is a pair of a {template} and a {condition}. The
        {template} is an instance of a table row with all fields that require update having
        values that are not {None}. The {condition} is an expression that identifies the
        portion of the table that will be affected
        """
        # go through the {specifications}
        for template, condition in specifications:
            # build the sql statement for this update
            sql = tuple(self.sql.updateRecords(template=template, condition=condition))
            # a template that sets nothing builds no statement
            if not sql:
                # so there is nothing to execute
                continue
            # otherwise, execute it
            self.execute(*sql)
        # all done
        return

    def delete(self, table, condition):
        """
        Delete all {table} records that match {condition}
        """
        # build the sql statements
        sql = self.sql.deleteRecords(table=table, condition=condition)
        # and execute
        return self.execute(*sql)

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
    def _commit(self):
        """
        Make the work of the transaction of a transaction block permanent
        """
        # tell the back end
        self.execute(*self.sql.commit())
        # all done
        return

    # meta methods
    # context manager support
    def __enter__(self):
        """
        Hook invoked when the context manager is entered: the block is a transaction
        """
        # begin the transaction
        self.execute(*self.sql.transaction())
        # and hand me back to the caller
        return self

    def __exit__(self, exc_type, exc_instance, exc_traceback):
        """
        Hook invoked when the context manager's block exits: a block that ends normally commits
        its transaction, and one that raises rolls it back
        """
        # if the block ended normally
        if exc_type is None:
            # commit the transaction
            self._commit()
        # otherwise
        else:
            # roll it back
            self.execute(*self.sql.rollback())
        # and re-raise any exception that occurred in the block
        return False


# end of file
