# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# orthologue
# (c) 1998-2015 all rights reserved
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


    # constants
    type = socket.SOCK_STREAM


    # input/output
    def read(self, minlen, maxlen=0):
        """
        Read {count} bytes from my input channel
        """
        # {minlen} must be the first argument for the following to work correctly
        # reset the result
        bstr = b''
        # adjust the inputs
        if maxlen < minlen: maxlen = minlen
        # try as many times as it takes
        while len(bstr) < minlen:
            # to pull data from the stream
            bstr += self.recv(maxlen-len(bstr))
        # return the bytes
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
