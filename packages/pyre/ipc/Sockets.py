# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import pyre

# my protocol
from .Transport import Transport

# the channel i deal in
from .SocketPair import SocketPair


# declaration
class Sockets(pyre.component, family="pyre.ipc.transports.socket", implements=Transport):
    """
    The transport that connects processes with unix domain socket pairs

    Beyond what pipes offer, these channels can carry open file descriptors between the two
    processes, and use half the descriptors
    """

    # interface
    @pyre.export
    def open(self, **kwds):
        """
        Build a pair of connected channels over a fresh unix domain socket pair
        """
        # delegate to the channel
        return SocketPair.open(**kwds)

    @pyre.export
    def wrap(self, descriptor, **kwds):
        """
        Dress the already open {descriptor} of one end of a connected pair as a channel
        """
        # dress it up
        return SocketPair(SocketPair.family, SocketPair.type, 0, fileno=descriptor, **kwds)


# end of file
