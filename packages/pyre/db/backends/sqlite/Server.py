# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
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
    def _send(self, statement, arguments=()):
        """
        Hand {statement} to my cursor, with the values in {arguments}, and report what sqlite
        thinks of it with the exceptions of the package
        """
        # a statement sent through a connection that was never opened
        if self.cursor is None:
            # is worth naming
            raise exceptions.InterfaceError(diagnostic="this server is not attached")
        # attempt to
        try:
            # execute the statement
            self.cursor.execute(statement, arguments)
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
        # the cursor holds the rows the statement makes
        return self.cursor

    # private data
    cursor = None  # the cursor that executes my statements
    connection = None  # my connection to the database


# end of file
