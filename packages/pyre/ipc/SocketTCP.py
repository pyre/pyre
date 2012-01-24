# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import socket
# my interface
from .Socket import Socket


# declaration
class SocketTCP(Socket):
    """
    A channel that uses TCP sockets as the communication mechanism
    """


    # types
    from ..schema import inet
    # constants
    type = socket.SOCK_STREAM


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


# end of file 
