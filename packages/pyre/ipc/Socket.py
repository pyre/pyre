# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import socket
# my interface
from .Channel import Channel


# declaration
class Socket(Channel):
    """
    A channel that uses sockets as the communication mechanism

    This class captures the part of the {socket} interface that is independent of the type of
    socket. The implementation of the remainder of the {Channel} interface is provided by
    subclasses.
    """


    # interface
    def close(self):
        """
        Shutdown my channel
        """
        # release the socket
        self.socket.close()
        # and return
        return


    # access to the individual channel end points
    @property
    def inbound(self):
        """
        Retrieve the channel end point that can be read
        """
        # easy enough
        return self.socket


    @property
    def outbound(self):
        """
        Retrieve the channel end point that can be written
        """
        # easy enough
        return self.socket


    # meta methods
    def __init__(self, socket, **kwds):
        super().__init__(**kwds)
        self.socket = socket
        return


    # private data
    socket = None


# end of file 
