# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pyre
import socket
# my interface
from .interfaces import channel


# declaration
class Socket(pyre.component, family="pyre.ipc.channels.socket", implements=channel):
    """
    A channel that uses sockets as the communication mechanism
    """


    # types
    from ..schema.INet import (
        Address as address,
        IPv4 as ipv4,
        Unix as unix
        )


    # interface
    # life cycle management
    @pyre.export
    @classmethod
    def open(cls, address, **kwds):
        """
        Create a socket channel
        """
        # recognize the address
        if not isinstance(address, cls.address):
            raise NotImplementedError("NYI: convert string to a socket address")

        # make a low level socket
        s = socket.socket(address.family)
        # connect
        s.connect(address.value)
        # wrap and return
        return cls(socket=s, **kwds)


    @pyre.export
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


    @pyre.export
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


    # input/output
    @pyre.export
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
