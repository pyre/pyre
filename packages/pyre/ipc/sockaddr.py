# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# externals
import socket


# the base class; useful for detecting address specifications that have already been cast to an
# address instance
class Address:
    """
    Base class for addresses
    """


class IPv4(Address):
    """
    Encapsulation of an ipv4 socket address
    """

    # public data
    family = socket.AF_INET
    host = ""
    port = 0

    @property
    def value(self):
        """
        Build the tuple required by {socket.connect}
        """
        return (self.host, self.port)

    # meta methods
    def __init__(self, host, port, **kwds):
        super().__init__(**kwds)
        self.host = host
        self.port = port
        return


class Unix(Address):
    """
    Unix domain sockets
    """

    # public data
    family = socket.AF_UNIX
    path = None

    @property
    def value(self):
        """
        Build the value expected by {socket.connect}
        """
        return self.path

    # meta methods
    def __init__(self, path, **kwds):
        super().__init__(**kwds)
        self.path = path
        return


# end of file 
