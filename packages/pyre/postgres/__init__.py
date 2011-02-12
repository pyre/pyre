# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Postgres import Postgres as database


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
