# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from .Operator import Operator


# the cell-wise product of two signals
class Multiply(pyre.flow.factory, family="pyre.viz.operators.multiply", implements=Operator):
    """
    The operator that multiplies two signals, sample by sample
    """

    # the inputs
    op1 = pyre.viz.tile.input()
    op1.doc = "the first operand"
    op2 = pyre.viz.tile.input()
    op2.doc = "the second operand"

    # the output
    product = pyre.viz.tile.output()
    product.doc = "the product of the two signals"


# end of file
