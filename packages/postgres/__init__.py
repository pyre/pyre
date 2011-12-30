# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# access to the data store implementation provided by this package
from .Postgres import Postgres as server


# package methods
# these are a bit too low level for most uses; please consider using postgres, the component
# that encapsulates access to the database back end
def connect(**kwds):
    """
    Establish a new connection to a database back end

    See the Connection class documentation for information on how to control the connection
    details through the arguments to this function
    """
    from .Connection import Connection
    return Connection(**kwds)


# end of file 
