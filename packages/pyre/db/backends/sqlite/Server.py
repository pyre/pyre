# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import contextlib
import datetime
import decimal
import pyre
import sqlite3

# superclass
from ... import Server as base

# my exceptions
from ... import exceptions

# the mill that speaks my dialect
from .Mill import Mill


# declaration
class Server(base.Server, family="pyre.db.servers.sqlite"):
    """
    Component that manages the connection to a sqlite database
    """

    # the exceptions that report the conditions sqlite names, by its primary result code
    conditions = {
        # a statement sqlite could not make sense of, or one about an object it does not have
        sqlite3.SQLITE_ERROR: exceptions.ProgrammingError,
        # a constraint the data violate
        sqlite3.SQLITE_CONSTRAINT: exceptions.IntegrityError,
        # values that do not fit
        sqlite3.SQLITE_MISMATCH: exceptions.DataError,
        sqlite3.SQLITE_TOOBIG: exceptions.DataError,
        # the circumstances of the database: its locks, its file, its permissions
        sqlite3.SQLITE_BUSY: exceptions.OperationalError,
        sqlite3.SQLITE_LOCKED: exceptions.OperationalError,
        sqlite3.SQLITE_READONLY: exceptions.OperationalError,
        sqlite3.SQLITE_IOERR: exceptions.OperationalError,
        sqlite3.SQLITE_FULL: exceptions.OperationalError,
        sqlite3.SQLITE_CANTOPEN: exceptions.OperationalError,
        sqlite3.SQLITE_PERM: exceptions.OperationalError,
        sqlite3.SQLITE_ABORT: exceptions.OperationalError,
        sqlite3.SQLITE_INTERRUPT: exceptions.OperationalError,
        sqlite3.SQLITE_PROTOCOL: exceptions.OperationalError,
        sqlite3.SQLITE_EMPTY: exceptions.OperationalError,
        sqlite3.SQLITE_SCHEMA: exceptions.OperationalError,
        sqlite3.SQLITE_NOLFS: exceptions.OperationalError,
        sqlite3.SQLITE_AUTH: exceptions.OperationalError,
        # damage to the database, or a failure of sqlite itself
        sqlite3.SQLITE_INTERNAL: exceptions.InternalError,
        sqlite3.SQLITE_CORRUPT: exceptions.InternalError,
        sqlite3.SQLITE_NOTADB: exceptions.InternalError,
        sqlite3.SQLITE_NOTFOUND: exceptions.InternalError,
        sqlite3.SQLITE_FORMAT: exceptions.InternalError,
        # a misuse of the interface of sqlite
        sqlite3.SQLITE_MISUSE: exceptions.InterfaceError,
        sqlite3.SQLITE_RANGE: exceptions.InterfaceError,
    }

    # the generator of my statements speaks the dialect of sqlite
    sql = pyre.weaver.language()
    sql.default = Mill
    sql.doc = "the generator of the SQL statements"

    # public state
    database = pyre.properties.str(default=":memory:")
    database.doc = "the path to the sqlite database"

    # interface
    @pyre.export
    def attach(self):
        """
        Connect to the database
        """
        # if i have an existing connection to the database
        if self.connection is not None:
            # there is nothing to do but hand me back
            return self
        # otherwise, make a connection in autocommit mode, so that each statement commits unless
        # a transaction was begun, as it does in postgres
        self.connection = sqlite3.connect(self.database, isolation_level=None)
        # and a cursor
        self.cursor = self.connection.cursor()
        # and return
        return self

    @pyre.export
    def detach(self):
        """
        Close the connection to the database
        """
        # if i don't have an existing connection to the database
        if self.connection is None:
            # there is nothing to do
            return
        # otherwise, close my cursor
        self.cursor.close()
        # and the connection
        self.connection.close()
        # reset the connection objects
        self.cursor = None
        self.connection = None
        # all done
        return

    @pyre.export
    def execute(self, *sql):
        """
        Execute the lines in {sql}, one statement at a time, since sqlite takes only one
        statement per call; the cursor holds the rows of the last one
        """
        # the lines of the statement being collected
        statement = []
        # go through the lines
        for line in sql:
            # add each one to the statement
            statement.append(line)
            # put it together
            text = "\n".join(statement)
            # and once sqlite says the statement is whole
            if sqlite3.complete_statement(text):
                # execute it
                self._send(statement=text)
                # and start the next one
                statement = []
        # lines that do not make a whole statement, such as a query without its terminator
        if statement:
            # are handed over as they are, so sqlite can say what it thinks of them
            self._send(statement="\n".join(statement))
        # return the cursor
        return self.cursor

    def run(self, statement, *arguments):
        """
        Execute a single {statement}, with its placeholders filled in by {arguments}, which
        travel beside it, so nothing they contain can change what the statement does
        """
        # hand it to the cursor, which holds the rows it makes
        return self._send(statement=statement, arguments=arguments)

    # bulk loading
    def load(self, *records):
        """
        Insert {records}, many at a time and all or nothing; the records of a table that give
        values for the same columns share one statement, which runs once for each of them
        """
        # the place that puts the values in the form the module takes
        parameters = self._parameters()
        # in a block of its own, so that the load keeps all of its records or none of them
        with self:
            # go through the groups of records
            for table, fields, group in self.sql.loadGroups(*records):
                # a group that leaves every column to the server
                if not fields:
                    # has no values to send, and is inserted as rows made of defaults
                    self.insert(*group)
                    # and that's all for it
                    continue
                # the statement of the group
                statement = self.sql.loadStatement(
                    table=table, fields=fields, parameters=parameters
                )
                # the values of each record, in the form the module takes
                rows = (
                    tuple(
                        parameters.bound(table=table, column=field, value=value)
                        for field, value in zip(
                            fields, self.sql.givenValues(table=table, record=record)
                        )
                    )
                    for record in group
                )
                # run it for each of them
                self._sendMany(statement=statement, rows=rows)
        # all done
        return self

    # prepared statements
    def _runPrepared(self, prepared, values, arguments):
        """
        Run the statement of {prepared}, with its placeholders filled in by {arguments}, and
        hand back the rows it makes; the module keeps the statements it has compiled, by their
        text, so a statement that comes back is not compiled again
        """
        # the text, as it was rendered
        statement = "\n".join(prepared.lines)
        # a statement that hands back no rows
        if prepared.selection is None:
            # runs as any other
            return self.run(statement, *arguments)
        # the others are read through a cursor of their own
        return self._read(statement=statement, arguments=arguments)

    # the values that travel beside my statements
    def _parameters(self):
        """
        Make a place for the values of a statement, which travel beside it
        """
        # my mill knows what they look like
        return self.sql.parameters()

    # the handlers of the columns whose values sqlite keeps in a form of its own
    def _pyre_onBoolean(self, schema, value, **kwds):
        """
        Turn {value}, the integer sqlite keeps for a truth value, into one
        """
        # easy enough
        return bool(value)

    def _pyre_onDecimal(self, schema, value, **kwds):
        """
        Turn {value}, the number sqlite keeps for a fixed point one, into one
        """
        # through its text, so the conversion adds no digits of its own
        return decimal.Decimal(str(value))

    def _pyre_onDate(self, schema, value, **kwds):
        """
        Turn {value}, the text sqlite keeps for a date, into one
        """
        # the text is the ISO form the dialect writes
        return datetime.date.fromisoformat(value)

    def _pyre_onTime(self, schema, value, **kwds):
        """
        Turn {value}, the text sqlite keeps for a time of day, into one
        """
        # the text is the ISO form the dialect writes
        return datetime.time.fromisoformat(value)

    def _pyre_onTimestamp(self, schema, value, **kwds):
        """
        Turn {value}, the text sqlite keeps for a moment, into one
        """
        # the text is the ISO form the dialect writes
        return datetime.datetime.fromisoformat(value)

    # implementation details
    def _fetch(self, lines, values, parameters):
        """
        Run the selection whose lines are {lines}, with {values} beside it, and hand back its
        rows, {batch} at a time, as they are read; other statements may run in the meantime
        """
        # read the rows through a cursor of their own
        return self._read(statement="\n".join(lines), arguments=values)

    def _read(self, statement, arguments):
        """
        Execute {statement}, with the values in {arguments}, through a cursor of its own, and
        hand back the rows it makes, as they are read
        """
        # while listening for complaints
        with self._complaints(statement=statement):
            # make a cursor for the statement
            cursor = self.connection.cursor()
        # carefully
        try:
            # while listening for complaints
            with self._complaints(statement=statement):
                # execute the statement
                cursor.execute(statement, arguments)
        # a statement that fails
        except exceptions.DatabaseError:
            # has no rows to read, so its cursor goes now
            cursor.close()
            # and the failure is reported
            raise
        # hand over its rows
        return self._rows(cursor=cursor, statement=statement)

    def _rows(self, cursor, statement):
        """
        Generate the rows of {statement} that {cursor} reads, {batch} at a time, and close it
        when they run out or the reading is abandoned
        """
        # the number of rows in a batch
        batch = self.batch
        # carefully
        try:
            # until the rows run out
            while True:
                # while listening for complaints
                with self._complaints(statement=statement):
                    # fetch the next batch
                    rows = cursor.fetchmany(batch)
                # an empty batch
                if not rows:
                    # means there are no more
                    break
                # hand over the rows of the others
                yield from rows
        # however the reading ends
        finally:
            # the cursor is no longer needed
            cursor.close()
        # all done
        return

    def _send(self, statement, arguments=()):
        """
        Hand {statement} to my cursor, with the values in {arguments}, and report what sqlite
        thinks of it with the exceptions of the package
        """
        # while listening for complaints
        with self._complaints(statement=statement):
            # execute the statement
            self.cursor.execute(statement, arguments)
        # the cursor holds the rows the statement makes
        return self.cursor

    def _sendMany(self, statement, rows):
        """
        Hand {statement} to my cursor once for each of {rows}, the values of its placeholders,
        and report what sqlite thinks of it with the exceptions of the package
        """
        # while listening for complaints
        with self._complaints(statement=statement):
            # execute the statement for each row
            self.cursor.executemany(statement, rows)
        # the cursor holds what the statement did
        return self.cursor

    @contextlib.contextmanager
    def _complaints(self, statement):
        """
        Run a block that hands {statement} to my cursor, and report what sqlite thinks of it with
        the exceptions of the package
        """
        # a statement sent through a connection that was never opened
        if self.cursor is None:
            # is worth naming
            raise exceptions.InterfaceError(diagnostic="this server is not attached")
        # attempt to
        try:
            # run the block
            yield
        # the module that binds sqlite complains about the use of its interface on its own, with
        # no result code, since sqlite never saw the statement
        except sqlite3.ProgrammingError as error:
            # so its complaint is reported as it is
            raise exceptions.ProgrammingError(diagnostic=str(error), command=statement) from None
        # every other complaint comes from sqlite, and its primary result code names the condition
        except sqlite3.Error as error:
            # look up the exception that reports it
            kind = self.conditions.get(error.sqlite_errorcode & 0xFF, exceptions.DatabaseError)
            # and raise it, with the name sqlite gives the condition in full
            raise kind(
                diagnostic=str(error), command=statement, code=error.sqlite_errorname
            ) from None
        # all done
        return

    # private data
    cursor = None  # the cursor that executes my statements; each selection reads through its own
    connection = None  # my connection to the database


# end of file
