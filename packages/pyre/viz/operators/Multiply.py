# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Binary import Binary


# the product of two quantities
class Multiply(pyre.flow.factory, family="pyre.viz.operators.multiply", implements=Binary):
    """
    The operator that multiplies two quantities: a tile scaled by a scalar, on either side, or
    two scalars; the tiles are a vector space over the scalars, so the product of two tiles is
    not among them
    """

    # the inputs
    op1 = pyre.viz.quantity.input()
    op1.doc = "the first factor"
    # and the second factor
    op2 = pyre.viz.quantity.input()
    op2.doc = "the second factor"

    # the output
    result = pyre.viz.quantity.output()
    result.doc = "the product of the two factors"

    # the c++ templates whose instantiations do my work, when a recipe is staged
    pyre_engines = ("pyre::flow::factories::operators::multiply_t",)


# end of file
