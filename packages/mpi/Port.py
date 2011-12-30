# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# superclasses
from .Object import Object


# declaration
class Port(Object):
    """
    A simple point-to-point communication conduit for two processes
    """


    # per-instance public data
    cpmmunicator = None # the communicator my peer and I belong to
    peer = None # my peer process
    tag = None # integer to use as a message tag 


    # class interface
    def receiveString(self):
        """
        Receive a string from my peer
        """
        # pass the back to the extension module
        return self.mpi.receiveString(self.communicator.handle, self.peer, self.tag)


    def sendString(self, string):
        """
        Send a string to my peer
        """
        # pass the back to the extension module
        return self.mpi.sendString(self.communicator.handle, self.peer, self.tag, string)


    # meta methods
    def __init__(self, **kwds):
        # chain to my ancestors
        super().__init__(**kwds)

        self.communicator = communicator
        self.peer = peer
        self.tag = tag

        # all done
        return


# end of file 
