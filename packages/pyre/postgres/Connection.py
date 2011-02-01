# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# helper routine to initialize the extension module
def initializeExtension():
    # access the extension
    from . import pyrepg
    # get hold of the standard compliant exception hierarchy
    from ..db import exceptions
    # register the exception hierarchy with the module so that the exceptions it raises are
    # subclasses of the ones defined in pyre.db
    pyrepg.registerExceptions(exceptions)
    # and return the module
    return pyrepg


# declaration
class Connection:
    """
    This is a sample documentation string for class Connection
    """


    # class public data
    pyrepg = initializeExtension() # the handle to the postgres extension module


    # meta methods
    def __init__(self, **kwds):
        # chain to the ancestors
        super().__init__(**kwds)
        # establish a connection
        connection = self.pyrepg.connect()

        # all done
        return


# end of file 
