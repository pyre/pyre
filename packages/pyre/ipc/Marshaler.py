# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import pyre


# declaration
class Marshaler(pyre.protocol, family="pyre.ipc.marshalers"):
    """
    Protocol for components responsible for serializing python objects for transmission to
    other processes
    """

    # factory for my default implementation
    @classmethod
    def pyre_default(cls, **kwds):
        """
        The marshaler to use when nobody asks for a specific one
        """
        # get the pickler
        from .Pickler import Pickler

        # and hand it off
        return Pickler

    # interface
    @pyre.provides
    def recv(self, channel):
        """
        Extract and return one object from {channel}

        Implementations raise {exceptions.EndOfStream} when the channel closes before a
        complete message arrives, so clients can tell a dead peer from a bad payload, and
        {exceptions.ArrivalError} when a message arrives without all of its descriptors, after
        consuming the whole of it
        """

    @pyre.provides
    def send(self, item, channel):
        """
        Pack and ship {item} over {channel}, and hand back the manifest of the message, which
        names the channels that travelled inside it
        """


# end of file
