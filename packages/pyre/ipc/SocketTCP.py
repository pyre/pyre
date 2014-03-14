# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# orthologue
# (c) 1998-2014 all rights reserved
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
    from ..schemata import inet
    # constants
    type = socket.SOCK_STREAM


    # input/output
    def read(self, count):
        """
        Read {count} bytes from my input channel
        """
        # read bytes
        bstr = self.recv(count)
        # in as many attempts as it takes
        while len(bstr) < count: bstr += self.recv(count-len(bstr))
        # and return them
        return bstr


    def write(self, bstr):
        """
        Write the bytes in {bstr} to my output channel
        """
        # make sure the entire byte string is delivered
        self.sendall(bstr)
        # and return the number of bytes sent
        return len(bstr)


    # implementation details
    __slots__ = () # socket has it, so why not...


# end of file 
