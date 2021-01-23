# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# externals
import operator
# superclass
from .Comparison import Comparison


# op>=
class GreaterEqual(Comparison):
    """
    Constraint that is satisfied when a candidate is greater than or equal to a given value
    """


    # my comparison
    compare = operator.ge
    # my tag
    tag = "greater than or equal to"


# end of file
