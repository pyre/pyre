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
    def createDatabase(self, name):
        """
        Build and execute the SQL statement to create the database {name}
        """
        # build the sql statement
        sql = self.sql.createDatabase(name=name)
        # and execute it
        return self.execute(*sql)

    def dropDatabase(self, name):
        """
        Build and execute the SQL statement to drop the database {name}
        """
        # build the sql statement
        sql = self.sql.dropDatabase(name=name)
        # and execute it
        return self.execute(*sql)

    def createTable(self, table):
        """
        Build and execute the SQL statement necessary to create {table}
        """
        # build the sql statement
        sql = self.sql.createTable(table)
        # and execute it
        return self.execute(*sql)

    def dropTable(self, table):
        """
        Build and execute the SQL statement necessary to delete {table} from the datastore
        """
        # build the sql statement
        sql = self.sql.dropTable(table)
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

    def select(self, query):
        """
        Execute the given {query} and return the retrieved data
        """
        # build the sql statements
        sql = self.sql.select(query=query)

        # the columns of the selection, one for each field of the query
        columns = query.pyre_fields
        # walk the rows the back end sent, which are data rows and nothing else
        for row in self.execute(*sql):
            # turn each value into the type of its column
            values = (
                self.interpret(column=column, value=value) for column, value in zip(columns, row)
            )
            # and build the row out of them, as they are
            yield query.pyre_storedTuple(record=query, data=values)

        # all done
        return

    # reading
    def interpret(self, column, value):
        """
        Turn {value}, which the back end sent for {column}, into the type of the column
        """
        # {NULL} is {None}, whatever the column
        if value is None:
            # so leave it alone
            return None
        # otherwise, let the column say what it is
        return column._pyre_identify(authority=self, value=value)

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
            self.execute(*self.sql.commit())
        # otherwise
        else:
            # roll it back
            self.execute(*self.sql.rollback())
        # and re-raise any exception that occurred in the block
        return False


# end of file
