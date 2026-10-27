# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Scalar import Scalar as scalar


# the implementations
@pyre.foundry(implements=scalar, tip="a product that holds a single number")
def variable():
    """ """
    # pull the implementation
    from .Variable import Variable

    # and publish it
    return Variable


# end of file
