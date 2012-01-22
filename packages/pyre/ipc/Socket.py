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
    A channel that uses TCP sockets as the communication mechanism
    """


    # interface
    def close(self):
        """
        Shutdown my channel
        """
        # shutdown the connection
        self.socket.shutdown(socket.SHUT_RDWR)
        # release the associated resources
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


    # input/output
    def read(self, count):
        """
        Read {count} bytes from my input channel
        """
        # read bytes
        bstr = self.socket.recv(count)
        # in as many attempts as it takes
        while len(bstr) < count: bstr += self.socket.recv(count-len(bstr))
        # and return them
        return bstr


    def write(self, bstr):
        """
        Write the bytes in {bstr} to my output channel
        """
        # make sure the entire byte string is delivered
        self.socket.sendall(bstr)
        # and return the number of bytes sent
        return len(bstr)


    # meta methods
    def __init__(self, socket, **kwds):
        super().__init__(**kwds)
        self.socket = socket
        return


    # private data
    socket = None


# end of file 
