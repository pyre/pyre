# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pyre
# superclass
from .Server import Server


# helper routine to initialize the extension module
def initializeExtension():
    # access the extension
    from ..extensions import postgres
    # get hold of the standard compliant exception hierarchy
    from pyre.db import exceptions
    # register the exception hierarchy with the module so that the exceptions it raises are
    # subclasses of the ones defined in pyre.db
    postgres.registerExceptions(exceptions)
    # and return the module
    return postgres


# declaration
class Postgres(Server, family="pyre.db.server.postgres"):
    """
    Component that manages the connection to a Postgres database
    """

    # exceptions
    from pyre.db.exceptions import OperationalError


    # public state
    database = pyre.properties.str(default="postgres")
    database.doc = "the name of the database to connect to"

    username = pyre.properties.str(default=None)
    username.doc = "the username to use for the connection"

    password = pyre.properties.str(default=None)
    password.doc = "the password to use for the connection"


    # interface
    @pyre.export
    def attach(self):
        """
        Connect to the database
        """
        # build the connection specification string
        spec = [
            ['dbname', self.database]
            ]
        if self.username is not None: spec.append(['user', self.username])
        if self.password is not None: spec.append(('password', self.password))
        # if application is not None: spec.append(('application_name', application))
        spec = ' '.join([ '='.join(entry) for entry in spec ])
        
        # establish a connection
        self.connection = self.postgres.connect(spec)
        # all done
        return self


    @pyre.export
    def detach(self):
        """
        Close the connection to the database

        Closing a connection makes it unsuitable for any further database access. This applies
        to all objects that may retain a reference to the connection being closed. Any
        uncommitted changes will be lost
        """
        return self.postgres.disconnect(self.connection)


    @pyre.export
    def execute(self, *sql):
        """
        Execute the sequence of SQL statements in {sql} as a single command
        """
        return self.postgres.execute(self.connection, "\n".join(sql))


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # initialize the extension module, if necessary
        if type(self).postgres is None: type(self).postgres = initializeExtension()
        # my private state
        self.connection = None

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


    # implementation details
    postgres = None # the handle to the extension module


# end of file 
