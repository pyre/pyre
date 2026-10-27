# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Binary import Binary


# the difference of two quantities
class Subtract(pyre.flow.factory, family="pyre.viz.operators.subtract", implements=Binary):
    """
    The operator that subtracts the second quantity from the first: two tiles, cell by cell; a
    tile and a scalar, on either side; or two scalars
    """

    # the inputs
    op1 = pyre.viz.quantity.input()
    op1.doc = "the quantity to subtract from"
    # and the quantity to take away
    op2 = pyre.viz.quantity.input()
    op2.doc = "the quantity to subtract"

    # the output
    result = pyre.viz.quantity.output()
    result.doc = "the first operand less the second"

    # the c++ templates whose instantiations do my work, when a recipe is staged
    pyre_engines = ("pyre::flow::factories::operators::subtract_t",)


# end of file
