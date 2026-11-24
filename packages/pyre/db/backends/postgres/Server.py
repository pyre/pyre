# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import pyre

# superclass
from ... import Server as base

# my exceptions
from ... import exceptions

# the mill that speaks my dialect
from .Mill import Mill


# declaration
class Server(base.Server, family="pyre.db.servers.postgres"):
    """
    Component that manages the connection to a Postgres database
    """

    # exceptions
    from ...exceptions import OperationalError

    # the condition postgres raises when a database it is asked to create exists already
    duplicateDatabase = "42P04"

    # the generator of my statements speaks the dialect of postgres
    sql = pyre.weaver.language()
    sql.default = Mill
    sql.doc = "the generator of the SQL statements"

    # public state
    # the database
    database = pyre.properties.str()
    database.default = "postgres"
    database.doc = "the name of the database to connect to"

    # who connects
    username = pyre.properties.str()
    username.default = None
    username.doc = "the database user name to use during authentication"

    # their password
    password = pyre.properties.str()
    password.default = None
    password.secret = True
    password.doc = "the password of the database user"

    # the name the server shows for this session
    application = pyre.properties.str()
    application.default = None
    application.doc = "the application name to use for the connection"

    # where the server is
    hostname = pyre.properties.str()
    hostname.default = None
    hostname.doc = "the host the database server is running on"

    # and the port it listens on
    port = pyre.properties.str()
    port.default = None
    port.doc = "the port the database server is listening on"

    # how talkative the server is
    quiet = pyre.properties.bool()
    quiet.default = True
    quiet.doc = "control whether certain postgres informationals are shown"

    # interface
    @pyre.export
    def attach(self):
        """
        Connect to the database
        """
        # if i have an existing connection to the back end
        if self.connection is not None:
            # there is nothing to do
            return self

        # get the bindings
        libpq = pyre.extensions.libpq
        # a build with no bindings cannot talk to a postgres server
        if libpq is None:
            # report it here, rather than let it surface as an attribute error below
            raise exceptions.NotSupportedError(
                diagnostic="this build of pyre has no postgres support"
            )

        # assemble the connection specification; each parameter is a name and a value, and the
        # two are kept apart all the way down to libpq, since a password with a space in it,
        # spliced into one string, would silently become a password and a garbage keyword. the
        # extension drops the entries whose value is {None}, so that libpq falls back on its own
        # defaults, which are better than any we could invent
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
        # if i don't have an existing connection to the back end
        if self.connection is None:
            # there is nothing to do
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

        The answer is the {Result} of the last statement: a sequence of rows, each of which is
        a sequence of values, with the names of the columns available separately, as
        {result.headers}
        """
        # a statement sent through a session that was never opened
        if self.connection is None:
            # is worth naming
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
        # a statement sent through a session that was never opened
        if self.connection is None:
            # is worth naming
            raise exceptions.InterfaceError(diagnostic="this server is not attached")

        # hand it to the session
        return self.connection.execute(statement, *arguments)

    # convenience
    def createDatabase(self, name, existOk=False):
        """
        Create the database {name}; with {existOk}, finding it there already is fine

        postgres has no syntax that creates a database only when it is missing, so i keep that
        promise myself: postgres decides whether the database exists as it runs the statement,
        and says so with a condition of its own
        """
        # build the statement that insists on making the database
        sql = self.sql.createDatabase(name=name)
        # attempt to
        try:
            # run it
            return self.execute(*sql)
        # if it fails
        except exceptions.ProgrammingError as error:
            # because the database is there already, which the caller said is fine
            if existOk and error.sqlstate == self.duplicateDatabase:
                # there is nothing to report
                return ()
            # anything else is a failure
            raise

    # the handlers of the columns whose values my bindings send in another form
    def _pyre_onJSON(self, schema, value, column, selection, **kwds):
        """
        Take {value}, a json document my bindings have read, or its text when the column is read
        as text
        """
        # a column read as its text
        if schema._asText:
            # holds the text of its documents
            return value
        # a document whose top level is text reads as text, and would be taken for it
        if isinstance(value, str):
            # so refuse it, and name the column
            raise exceptions.DataError(
                diagnostic=(
                    f"the column {selection.pyre_name}.{column.name} holds a document whose top "
                    "level is text; read it with asText"
                ),
                table=selection.pyre_name,
                column=column.name,
            )
        # every other document is taken as it is
        return value

    def _pyre_onArray(self, schema, value, **kwds):
        """
        Turn {value}, the list my bindings send for an array, into a tuple, level by level
        """
        # a level
        if isinstance(value, list):
            # becomes a tuple of its entries, each turned the same way
            return tuple(self._pyre_onArray(schema=schema, value=entry) for entry in value)
        # an entry is left alone
        return value

    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # my session with the back end, which does not exist until somebody attaches
        self.connection = None
        # all done
        return

    # implementation details
    def _commit(self):
        """
        Make the work of the transaction of a transaction block permanent, and say so when the
        server had abandoned the transaction instead
        """
        # tell the server
        result = self.execute(*self.sql.commit())
        # a transaction the server had already abandoned answers its commit with a rollback, and
        # with no error of its own
        if result.command == "ROLLBACK":
            # so say that nothing was kept
            raise exceptions.OperationalError(
                diagnostic="the transaction was rolled back, so none of its work was kept",
                command="COMMIT",
            )
        # all done
        return

    # private data
    connection = None  # my session with the back end


# end of file
