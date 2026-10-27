# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Binary import Binary


# the quotient of two quantities
class Divide(pyre.flow.factory, family="pyre.viz.operators.divide", implements=Binary):
    """
    The operator that divides the first quantity by the second: a tile by a scalar, or two
    scalars; the tiles are a vector space over the scalars, so nothing divides by a tile
    """

    # the inputs
    op1 = pyre.viz.quantity.input()
    op1.doc = "the dividend"
    # and the quantity to divide by
    op2 = pyre.viz.quantity.input()
    op2.doc = "the divisor, a scalar"

    # the output
    result = pyre.viz.quantity.output()
    result.doc = "the quotient"

    # the c++ templates whose instantiations do my work, when a recipe is staged
    pyre_engines = ("pyre::flow::factories::operators::divide_t",)


# end of file
