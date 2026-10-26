# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Binary import Binary


# the cell-wise sum of two signals
class Add(pyre.flow.factory, family="pyre.viz.operators.add", implements=Binary):
    """
    The operator that adds two signals, sample by sample
    """

    # the inputs
    op1 = pyre.viz.tile.input()
    op1.doc = "the first operand"
    op2 = pyre.viz.tile.input()
    op2.doc = "the second operand"

    # the output
    result = pyre.viz.tile.output()
    result.doc = "the sum of the two signals"

    # the c++ templates whose instantiations do my work, when a recipe is staged
    pyre_engines = ("pyre::flow::factories::operators::add_t",)


# end of file
