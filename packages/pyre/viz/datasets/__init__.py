# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Dataset import Dataset as dataset


# the implementations
@pyre.foundry(implements=dataset, tip="a dataset of a file, held in memory")
def memory():
    """
    A dataset of a file, held in memory
    """
    # pull the implementation
    from .Memory import Memory

    # and publish it
    return Memory


# end of file
