# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Binary import Binary


# the cell-wise difference of two signals
class Subtract(pyre.flow.factory, family="pyre.viz.operators.subtract", implements=Binary):
    """
    The operator that subtracts the second signal from the first, sample by sample
    """

    # the inputs
    op1 = pyre.viz.tile.input()
    op1.doc = "the signal to subtract from"
    # and the signal to take away
    op2 = pyre.viz.tile.input()
    op2.doc = "the signal to subtract"

    # the output
    result = pyre.viz.tile.output()
    result.doc = "the first signal less the second"

    # the c++ templates whose instantiations do my work, when a recipe is staged
    pyre_engines = ("pyre::flow::factories::operators::subtract_t",)


# end of file
