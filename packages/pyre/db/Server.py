# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import pyre
import pyre.weaver
from . import datastore, sql


# declaration
class Server(pyre.component, implements=datastore):
    """
    Abstract component that encapsulates the connection to a database back end

    This class is meant to be used as the base class for back end specific component
    implementations. It provides a complete but trivial implementation of the {DataStore}
    interface.
    """


    # traits
    sql = pyre.properties.facility(interface=pyre.weaver.language, default=sql)
    sql.doc = "the generator of the SQL statements"


    # required interface
    @pyre.export
    def attach(self):
        """
        Connect to the database back end
        """
        raise NotImplementedError(
            "class {.__class__.__name__!r} must override 'attach'".format(self))


    @pyre.export
    def execute(self, sql):
        """
        Execute the sequence of SQL statements in {sql} as a single command
        """
        raise NotImplementedError(
            "class {.__class__.__name__!r} must override 'execute'".format(self))


    # convenience
    def createTable(self, table):
        """
        Build and execute the SQL statement necessary to create {table}
        """
        # build the sql statement
        sql = self.sql.createTable(table)
        # and execute it
        return self.execute(sql)


    def dropTable(self, table):
        """
        Build and execute the SQL statement necessary to delete {table} from the datastore
        """
        # build the sql statement
        sql = self.sql.dropTable(table)
        # and execute it
        return self.execute(sql)


    def insert(self, *records):
        """
        Insert {items} into the database
        """
        # build the sql statements
        sql = self.sql.insertRecords(records)
        # and execute
        return self.execute(sql)
        

    # meta methods
    # context manager support
    def __enter__(self):
        """
        Hook invoked when the context manager is entered
        """
        return self


    def __exit__(self, exc_type, exc_instance, exc_traceback):
        """
        Hook invoked when the context manager's block exits
        """
        # re-raise any exception that occurred while executing the body of the with statement
        return False


# end of file 
