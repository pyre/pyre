# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# externals
import operator
# superclass
from .Comparison import Comparison


# op=
class Equal(Comparison):
    """
    Constraint that checks whether the candidate is equal to some value
    """


    # my comparison
    compare = operator.eq
    # and its textual representation
    tag = "equal to"


# end of file
