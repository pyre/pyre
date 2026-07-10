# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import pyre

# the bindings over {libpq}; {None} when this build has no postgres support
from ..extensions import libpq

# superclass
from .Server import Server

# my exceptions
from . import exceptions


# declaration
class Postgres(Server, family="pyre.db.server.postgres"):
    """
    Component that manages the connection to a Postgres database
    """

    # exceptions
    from .exceptions import OperationalError

    # public state
    database = pyre.properties.str(default="postgres")
    database.doc = "the name of the database to connect to"

    username = pyre.properties.str(default=None)
    username.doc = "the database user name to use during authentication"

    password = pyre.properties.str(default=None)
    password.doc = "the password of the database user"

    application = pyre.properties.str(default=None)
    application.doc = "the application name to use for the connection"

    hostname = pyre.properties.str(default=None)
    hostname.doc = "the host the database server is running on"

    port = pyre.properties.str(default=None)
    port.doc = "the port the database server is listening on"

    quiet = pyre.properties.bool(default=True)
    quiet.doc = "control whether certain postgres informationals are shown"

    # interface
    @pyre.export
    def attach(self):
        """
        Connect to the database
        """
        # if i have an existing connection to the back end, do nothing
        if self.connection is not None:
            return self

        # a build with no bindings cannot talk to a postgres server
        if libpq is None:
            # report it here, rather than let it surface as an attribute error below
            raise exceptions.NotSupportedError(
                diagnostic="this build of pyre has no postgres support"
            )

        # assemble the connection specification; each parameter is a name and a value, and the
        # two are kept apart all the way down to libpq. splicing them into one string, as this
        # component used to, means a password with a space in it silently becomes a password and
        # a garbage keyword. the extension drops the entries whose value is {None}, so that libpq
        # falls back on its own defaults, which are better than any we could invent
        spec = {
            "dbname": self.database,
            "user": self.username,
            "password": self.password,
            "application_name": self.application,
            "host": self.hostname,
            "port": self.port,
        }

        # establish the connection
        self.connection = libpq.Connection(spec)

        # if the user asked for {quiet} operation
        if self.quiet:
            # set the minimum diagnostic level to {warning}
            self.execute("SET client_min_messages = warning;")

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
        # if i don't have an existing connection to the back end, do nothing
        if self.connection is None:
            return

        # otherwise, close the connection; every copy of it observes this, so nothing that still
        # holds one can go on to use a session the server has already forgotten
        self.connection.close()
        # invalidate the member
        self.connection = None

        # all done
        return

    @pyre.export
    def execute(self, *sql):
        """
        Execute the sequence of SQL statements in {sql} as a single command

        The answer is a {Result}: a sequence of rows, each of which is a sequence of values,
        with the names of the columns available separately, as {result.headers}
        """
        # a statement sent through a session that was never opened is worth naming
        if self.connection is None:
            raise exceptions.InterfaceError(diagnostic="this server is not attached")

        # assemble the command and pass it on to the session. this is the simple protocol, so
        # the statements may be several; none of them may carry a placeholder, and none of them
        # may be built out of anything a user typed
        return self.connection.exec("\n".join(sql))

    def run(self, statement, *arguments):
        """
        Execute a single {statement}, with its $1, $2, ... placeholders filled in

        This is the safe way to put a value into a statement: the values travel beside the sql
        rather than inside it, so nothing they contain can change what the statement does
        """
        # a statement sent through a session that was never opened is worth naming
        if self.connection is None:
            raise exceptions.InterfaceError(diagnostic="this server is not attached")

        # hand it to the session
        return self.connection.execute(statement, *arguments)

    def transaction(self):
        """
        Build a context manager that opens a transaction on my connection

        The transaction commits when its block exits normally, and rolls back when the block
        raises
        """
        # a transaction on a session that was never opened is worth naming
        if self.connection is None:
            raise exceptions.InterfaceError(diagnostic="this server is not attached")

        # build one on my session
        return libpq.Transaction(self.connection)

    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # my session with the back end, which does not exist until somebody attaches
        self.connection = None
        # all done
        return

    # context manager interface
    def __enter__(self):
        """
        Hook invoked when the context manager is entered
        """
        # mark the beginning of a transaction
        self.execute(*self.sql.transaction())
        # and hand me back to the caller
        return self

    def __exit__(self, exc_type, exc_instance, exc_traceback):
        """
        Hook invoked when the context manager's block exits
        """
        # if there were no errors detected
        if exc_type is None:
            # commit the transaction to the datastore
            self.execute(*self.sql.commit())
        # otherwise
        else:
            # roll back
            self.execute(*self.sql.rollback())

        # indicate that we want to re-raise any exceptions that occurred while executing the
        # body of the {with} statement
        return False

    # implementation details
    connection = None  # my session with the back end


# end of file
