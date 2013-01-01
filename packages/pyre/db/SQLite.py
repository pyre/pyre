# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import pyre
import sqlite3
# superclass
from .Server import Server
from .Selection import Selection


# declaration
class SQLite(Server, family="pyre.db.server.sqlite"):
    """
    Component that manages the connection to a sqlite database
    """


    # types
    class selection(Selection):
        """override {__iter__}: sqlite does not return headers"""

        def __iter__(self):
            """
            Wrap each result tuple as record as return it
            """
            # iterate over the result set
            for result in self.results:
                # build and instance of the query embedded record type
                record = self.query.pyre_Record(raw=result)
                # return it to the caller
                yield record
            # all done
            return


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
