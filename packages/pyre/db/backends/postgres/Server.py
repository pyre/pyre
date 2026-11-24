# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import contextlib
import hashlib
import itertools
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
    # the one it raises when a lock is not granted in time
    lockNotAvailable = "55P03"
    # and the one it raises when a cursor is not there
    invalidCursorName = "34000"

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

        # the literals my mill writes double their quotes and leave backslashes alone, which is
        # how the language reads text; make sure the session reads it that way, whatever the
        # server, the database or the role was set up to do
        self.execute("SET standard_conforming_strings = on;")

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
        # the cursors waiting to be closed went with the session
        self._abandoned = []

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

    # bulk loading
    def load(self, *records):
        """
        Insert {records}, many at a time and all or nothing; the records of a table that give
        values for the same columns are copied into it together
        """
        # a load through a session that was never opened
        if self.connection is None:
            # is worth naming
            raise exceptions.InterfaceError(diagnostic="this server is not attached")
        # the place that puts the values in the form the bindings take
        parameters = self._parameters()
        # in a block of its own, so that the load keeps all of its records or none of them
        with self:
            # go through the groups of records
            for table, fields, group in self.sql.loadGroups(*records):
                # a group that leaves every column to the server
                if not fields:
                    # has no values to copy, and is inserted as rows made of defaults
                    self.insert(*group)
                    # and that's all for it
                    continue
                # the statement that starts the copy of the group
                statement = self.sql.copyStatement(table=table, fields=fields)
                # copy the group; the copy keeps its rows when the block ends, and the server
                # refuses them then, when it must
                with self.connection.copyIn(statement) as copy:
                    # go through the records
                    for record in group:
                        # and send the values of each, in the form the bindings take
                        copy.row(
                            *(
                                parameters.bound(table=table, column=field, value=value)
                                for field, value in zip(
                                    fields, self.sql.givenValues(table=table, record=record)
                                )
                            )
                        )
        # all done
        return self

    # locks
    @contextlib.contextmanager
    def lock(self, name, wait=True, timeout=None):
        """
        Hold the advisory lock {name}, a name or an integer, from the start of a block to its
        end, whatever the transactions inside it do; wait for it unless {wait} is off, and for no
        longer than {timeout} seconds when it is given
        """
        # the key of the lock
        key = self._lockKey(name=name)
        # take the lock
        self._lock(key=key, name=name, wait=wait, timeout=timeout)
        # carefully
        try:
            # hand control to the block
            yield self
        # and however it ends
        finally:
            # let go of the lock
            self.run("SELECT pg_advisory_unlock($1::bigint)", key)
        # all done
        return

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

    # the keys and the taking of locks
    def _lockKey(self, name):
        """
        Build the key of the lock {name}: an integer is a key already, and a name is turned into
        one by a hash every process computes the same way
        """
        # an integer
        if isinstance(name, int):
            # is a key already
            return name
        # the first eight bytes of the digest of the name
        digest = hashlib.blake2b(name.encode("utf-8"), digest_size=8).digest()
        # make the key, as postgres reads it
        return int.from_bytes(digest, "big", signed=True)

    def _lock(self, key, name, wait, timeout):
        """
        Take the lock {name}, whose key is {key}, waiting as {wait} and {timeout} allow
        """
        # a caller that will not wait
        if not wait:
            # asks for the lock
            ((taken,),) = self.run("SELECT pg_try_advisory_lock($1::bigint)", key)
            # and if it is held elsewhere
            if not taken:
                # says so
                raise exceptions.LockError(diagnostic=f"the lock {name} is held by another session")
            # otherwise, it holds it now
            return
        # a caller that waits as long as it takes
        if timeout is None:
            # waits
            self.run("SELECT pg_advisory_lock($1::bigint)", key)
            # until it holds it
            return
        # the others wait for no longer than the timeout, which postgres takes in milliseconds
        limit = f"{max(1, round(timeout * 1000))}ms"
        # the bound of the session, which the wait replaces for a moment
        ((previous,),) = self.run("SELECT current_setting('lock_timeout')")
        # whether the session is outside a transaction, which decides how the bound comes back
        idle = self.connection.transaction == pyre.extensions.libpq.TransactionStatus.idle
        # bound the wait
        self.run("SELECT set_config('lock_timeout', $1, false)", limit)
        # carefully
        try:
            # wait for the lock
            self.run("SELECT pg_advisory_lock($1::bigint)", key)
        # a lock not granted in time
        except exceptions.OperationalError as error:
            # is reported as such
            if error.sqlstate == self.lockNotAvailable:
                # with the name of the lock
                raise exceptions.LockError(
                    diagnostic=f"the lock {name} is held by another session"
                ) from None
            # and anything else as it is
            raise
        # either way
        finally:
            # a session outside a transaction gets its bound back now; inside one, a failed
            # wait has abandoned the transaction, and its rollback restores the bound
            if idle:
                # restore it
                self.run("SELECT set_config('lock_timeout', $1, false)", previous)
        # all done
        return

    # prepared statements
    def _runPrepared(self, prepared, values, arguments):
        """
        Run the statement of {prepared}, with its placeholders filled in by {arguments}, and
        hand back the rows it makes; the statement reaches the session on its first run, and
        again on the first run after i attach to a new session, which knows none of the old one's
        """
        # a statement sent through a session that was never opened
        if self.connection is None:
            # is worth naming
            raise exceptions.InterfaceError(diagnostic="this server is not attached")
        # a statement my session has not been taught
        if prepared.session is not self.connection:
            # gets a name of its own
            name = f"pyre_prepared_{next(self._prepared)}"
            # and is taught to the session under it
            self.connection.prepare(name, "\n".join(prepared.lines))
            # remember where it is
            prepared.name = name
            prepared.session = self.connection
        # run it
        return self.connection.execPrepared(prepared.name, *arguments)

    def _releasePrepared(self, prepared):
        """
        Make my session forget the statement of {prepared}, if it was taught it
        """
        # a statement taught to my current session
        if prepared.session is not None and prepared.session is self.connection:
            # is forgotten
            self.connection.release(prepared.name)
        # either way, the statement is taught nowhere now
        prepared.name = None
        prepared.session = None
        # all done
        return self

    # the values that travel beside my statements
    def _parameters(self):
        """
        Make a place for the values of a statement, which travel beside it
        """
        # my mill knows what they look like
        return self.sql.parameters()

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
        # the numbers that tell apart the names of the statements i prepare
        self._prepared = itertools.count(start=1)
        # and of the cursors my selections read through
        self._cursors = itertools.count(start=1)
        # the cursors abandoned while their session could not close them, each with its session
        self._abandoned = []
        # all done
        return

    # implementation details
    def _fetch(self, lines, values, parameters):
        """
        Run the selection whose lines are {lines}, with {values} beside it, through a cursor of my
        session, and generate its rows, {batch} at a time, as they are read; other statements may
        run in the meantime, and the cursor is closed when the rows run out or the reading is
        abandoned; the cursors earlier selections had to leave behind are closed first
        """
        # a selection sent through a session that was never opened
        if self.connection is None:
            # is worth naming
            raise exceptions.InterfaceError(diagnostic="this server is not attached")
        # the session that holds the cursor
        session = self.connection
        # the cursors abandoned while the session could not close them
        abandoned, self._abandoned = self._abandoned, []
        # get closed now, if the session can and still has them
        for owner, cursor in abandoned:
            # one at a time
            self._closeCursor(session=owner, name=cursor)
        # the new cursor gets a name of its own
        name = f"pyre_cursor_{next(self._cursors)}"
        # and is declared over the selection, with its values
        session.execute("\n".join(self.sql.declareCursor(name=name, selection=lines)), *values)
        # the number of rows in a batch
        batch = self.batch
        # and the statement that fetches them
        fetch = "\n".join(self.sql.fetchFromCursor(name=name, count=batch))
        # carefully
        try:
            # until the rows run out
            while True:
                # fetch the next batch
                rows = session.exec(fetch)
                # hand over its rows
                yield from rows
                # and if it fell short
                if len(rows) < batch:
                    # it was the last
                    break
        # however the reading ends
        finally:
            # the cursor is no longer needed
            self._closeCursor(session=session, name=name)
        # all done
        return

    def _closeCursor(self, session, name):
        """
        Close the cursor {name} of {session}, when the session can run the statement and still
        has the cursor
        """
        # a session that is no longer mine has hung up, which closed its cursors
        if session is not self.connection:
            # so there is nothing to close
            return
        # a session whose transaction has failed runs nothing until the transaction rolls back;
        # the rollback takes a cursor that was declared in the transaction, and leaves one
        # declared before it to the session
        if session.transaction == pyre.extensions.libpq.TransactionStatus.inError:
            # so the cursor waits for my next selection, which closes it if it is still there
            self._abandoned.append((session, name))
            # and that is all for now
            return
        # carefully
        try:
            # close the cursor
            session.exec("\n".join(self.sql.closeCursor(name=name)))
        # if the session no longer has it
        except exceptions.OperationalError as error:
            # because it was declared in a transaction that rolled back and took it, all is well;
            # anything else is a failure
            if error.sqlstate != self.invalidCursorName:
                # so report it
                raise
        # all done
        return

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
