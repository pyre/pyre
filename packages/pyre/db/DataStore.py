# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import pyre


# declaration
class DataStore(pyre.interface, family="pyre.db.server"):
    """
    Interface declaration for database managers
    """


    # interface
    @pyre.provides
    def attach(self):
        """
        Establish a connection to the indicated data store
        """


# end of file 
