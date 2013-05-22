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


# declaration
class Less(Comparison):
    """
    Constraint that checks whether the candidate is less than some value
    """

    # my comparison
    compare = operator.lt
    # and its textual representation
    tag = "less than"


# end of file 
