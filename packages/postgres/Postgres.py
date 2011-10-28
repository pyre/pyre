# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# package access
import pyre.db 


# declaration
class Postgres(pyre.db.server, family="postgres.server"):
    """
    Component that manages the connection to a Postgres database
    """

    # public state
    database = pyre.properties.str(default="postgres")
    database.doc = "the name of the database to connect to"

    username = pyre.properties.str(default=None)
    username.doc = "the username to use for the connection"

    password = pyre.properties.str(default=None)
    password.doc = "the password to use for the connection"


    # exceptions
    from pyre.db.exceptions import OperationalError


    # interface
    @pyre.export
    def attach(self):
        """
        Connect to the database
        """
        # get access to the connection object
        from .Connection import Connection
        # create a connection
        self._connection = Connection(
            database=self.database, user=self.username, password=self.password
            )
        # all done
        return self


    def execute(self, *sql):
        """
        Execute the sequence of SQL statements in {sql} as a single command
        """
        return self._connection.execute("\n".join(sql))


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # my private state
        self._connection = None

        return


    # context manager interface
    def __enter__(self):
        """
        Hook invoked when the context manager is entered
        """
        status = self.execute(*self.sql.transaction())
        return self


    def __exit__(self, exc_type, exc_instance, exc_traceback):
        """
        Hook invoked when the context manager's block exits
        """
        if exc_type is None:
            status = self.execute(*self.sql.commit())
        else:
            status = self.execute(*self.sql.rollback())

        # re-raise any exception that occurred while executing the body of the with statement
        return False


# end of file 
