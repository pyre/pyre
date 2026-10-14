# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Contents import Contents as contents


# the implementations
@pyre.foundry(implements=contents, tip="the contents of a file, held in memory")
def memory():
    """
    The contents of a file, held in memory
    """
    # pull the implementation
    from .Memory import Memory

    # and publish it
    return Memory


# end of file
