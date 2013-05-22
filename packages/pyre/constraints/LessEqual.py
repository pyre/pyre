# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import operator
# superclass
from .Comparison import Comparison


class LessEqual(Comparison):
    """
    Constraint that is satisfied if the candidate is less than or equal to a given value
    """


    # my comparison
    compare = operator.le
    # and its textual representation
    tag = "less than or equal to"


# end of file 
