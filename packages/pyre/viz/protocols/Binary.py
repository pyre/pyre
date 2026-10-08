# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Operator import Operator


# the operators that take two inputs; a building block of the operators, with no family of its own,
# so it takes no part in resolving names or in finding the components that implement the
# operators
class Binary(Operator):
    """
    The protocol of the binary operators: pointwise functions of two inputs
    """


# end of file
