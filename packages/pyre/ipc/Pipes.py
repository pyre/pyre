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
from .Pipe import Pipe


# declaration
class Pipes(pyre.component, family="pyre.ipc.transports.pipe", implements=Transport):
    """
    The transport that connects processes with pipes
    """

    # interface
    @pyre.export
    def open(self, **kwds):
        """
        Build a pair of connected channels, each backed by a pair of pipes
        """
        # delegate to the channel
        return Pipe.open(**kwds)

    @pyre.export
    def wrap(self, infd, outfd, **kwds):
        """
        Dress the already open descriptors {infd} and {outfd} as a channel
        """
        # dress them up
        return Pipe(infd=infd, outfd=outfd, **kwds)


# end of file
