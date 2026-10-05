# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from .Operator import Operator


# the cell-wise sum of two signals
class Add(pyre.flow.factory, family="pyre.viz.operators.add", implements=Operator):
    """
    The operator that adds two signals, sample by sample
    """

    # the inputs
    op1 = pyre.viz.tile.input()
    op1.doc = "the first operand"
    op2 = pyre.viz.tile.input()
    op2.doc = "the second operand"

    # the output
    sum = pyre.viz.tile.output()
    sum.doc = "the sum of the two signals"


# end of file
