# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import pyre


# declaration
class Transport(pyre.protocol, family="pyre.ipc.transports"):
    """
    Protocol for components that build the channels over which processes talk to each other

    Transports deal in connected pairs: {open} builds both ends of a fresh conversation, and
    {wrap} dresses descriptors that already exist, e.g. ones inherited across an {exec} or
    received from a peer, as a channel
    """

    # factory for my default implementation
    @classmethod
    def pyre_default(cls, **kwds):
        """
        The default {Transport} implementation
        """
        # pipes are supported everywhere
        from .Pipes import Pipes

        # so publish them
        return Pipes

    # interface
    @pyre.provides
    def open(self, **kwds):
        """
        Build a pair of connected channels suitable for bidirectional communication between
        two processes on the same host, returned as labeled {ends}
        """

    @pyre.provides
    def wrap(self, **kwds):
        """
        Dress already open descriptors as a channel; the signature is mechanism specific
        """


# end of file
