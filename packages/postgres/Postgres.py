# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# package access
import pyre.db 


# declaration
class Postgres(pyre.db.server, family="pyre.db.postgres"):
    """
    Component that manages the connection to a Postgres database
    """

    # public state
    database = pyre.properties.str(default="postgres")
    database.doc = "the name of the database to connect to"

    username = pyre.properties.str(default=None)
    username.doc = "the username to use for the connection"

    password = pyre.properties.str(default=None)
    username.doc = "the password to use for the connection"


    # exceptions
    from pyre.db.exceptions import OperationalError


    # interface
    @pyre.export
    def attach(self):
        """
        Connect to the database
        """
        # get access to the connection object
        from .Connection import Connection
        # create a connection
        self._connection = Connection(
            database=self.database, user=self.username, password=self.password
            )
        # all done
        return


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # my private state
        self._connection = None

        return


# end of file 
