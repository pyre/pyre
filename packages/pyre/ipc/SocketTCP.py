# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


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

    # input/output is inherited from {Socket}, whose implementations assume stream semantics

    # meta-methods
    def __str__(self):
        """build a human readable representation"""
        return f"tcp socket to {self.peer}"

    # implementation details
    __slots__ = ()  # socket has it, so why not...


# end of file
