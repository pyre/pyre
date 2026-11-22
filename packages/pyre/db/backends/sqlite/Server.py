# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
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
            # there is nothing to do
            return
        # otherwise, make a connection
        self.connection = sqlite3.connect(self.database)
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
        Execute the sequence of SQL statements in {sql} as a single command
        """
        # splice the statements together and hand them to my cursor
        self.cursor.execute("\n".join(sql))
        # return the cursor
        return self.cursor

    # implementation details
    cursor = None  # the cursor that executes my statements
    connection = None  # my connection to the database


# end of file
