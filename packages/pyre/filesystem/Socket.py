# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# superclass
from .File import File


# class declaration
class Socket(File):
    """
    Representation of sockets, a type of interprocess communication mechanism
    """

    # constant
    marker = "s"

    # interface
    def identify(self, explorer, **kwds):
        """
        Tell {explorer} that it is visiting a socket
        """
        # dispatch
        return explorer.onSocket(info=self, **kwds)


# end of file
