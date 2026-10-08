# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Operator import Operator as operator


# the implementations
@pyre.foundry(implements=operator, tip="the cell-wise sum of two signals")
def add():
    """
    The cell-wise sum of two signals
    """
    # pull the implementation
    from .Add import Add

    # and publish it
    return Add


@pyre.foundry(implements=operator, tip="the cell-wise product of two signals")
def multiply():
    """
    The cell-wise product of two signals
    """
    # pull the implementation
    from .Multiply import Multiply

    # and publish it
    return Multiply


# end of file
