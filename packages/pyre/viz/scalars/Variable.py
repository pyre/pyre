# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Scalar import Scalar


# a scalar
class Variable(pyre.flow.product, family="pyre.viz.scalars.variable", implements=Scalar):
    """
    A product that holds a single number
    """


# end of file
