# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Binary import Binary


# the sum of two quantities
class Add(pyre.flow.factory, family="pyre.viz.operators.add", implements=Binary):
    """
    The operator that adds two quantities: two tiles, cell by cell; a tile and a scalar, on
    either side, which adds the scalar to every cell; or two scalars
    """

    # the inputs
    op1 = pyre.viz.quantity.input()
    op1.doc = "the first operand"
    # and the second operand
    op2 = pyre.viz.quantity.input()
    op2.doc = "the second operand"

    # the output
    result = pyre.viz.quantity.output()
    result.doc = "the sum of the two operands"

    # the c++ templates whose instantiations do my work, when a recipe is staged
    pyre_engines = ("pyre::flow::factories::operators::add_t",)


# end of file
