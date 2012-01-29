# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pyre
import sqlite3
# superclass
from .Server import Server


# declaration
class SQLite(Server, family="pyre.db.server.sqlite"):
    """
    Component that manages the connection to a sqlite database
    """


    # public state
    database = pyre.properties.str(default=":memory:")
    database.doc = "the path to the sqlite database"


    # interface
    @pyre.export
    def attach(self):
        """
        Connect to the database
        """
        # make a connection
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
        # close the cursor
        self.cursor.close()
        # all done
        return


    @pyre.export
    def execute(self, *sql):
        """
        Execute the sequence of SQL statements in {sql} as a single command
        """
        # splice the statements together and hand them to my cursor
        self.cursor.execute('\n'.join(sql))
        # return the cursor
        return self.cursor


    # implementation details
    cursor = None
    connection = None

# end of file 
