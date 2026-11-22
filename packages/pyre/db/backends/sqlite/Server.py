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

# the mill that speaks my dialect
from .Mill import Mill


# declaration
class Server(base.Server, family="pyre.db.servers.sqlite"):
    """
    Component that manages the connection to a sqlite database
    """

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
                self.cursor.execute(text)
                # and start the next one
                statement = []
        # lines that do not make a whole statement, such as a query without its terminator
        if statement:
            # are handed over as they are, so sqlite can say what it thinks of them
            self.cursor.execute("\n".join(statement))
        # return the cursor
        return self.cursor

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
    cursor = None  # the cursor that executes my statements
    connection = None  # my connection to the database


# end of file
