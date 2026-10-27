# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Quantity import Quantity


# the protocol for scalars
class Scalar(Quantity, family="pyre.viz.scalars"):
    """
    The protocol for products that hold a single number, such as a scale or a shift; a scalar
    has no shape, and whatever factory is bound to it decides its value
    """

    # the c++ product templates whose instantiations satisfy me
    pyre_products = ("pyre::flow::products::var_t",)

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Provide a default implementation of scalars
        """
        # use a variable
        from ..scalars.Variable import Variable

        # publish
        return Variable


# end of file
