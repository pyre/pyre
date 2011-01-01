# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import functools
from .Polyadic import Polyadic


class Reductor(Polyadic):
    """
    Base class for reductive evaluators, i.e., they apply an operator on a pair of nodes at a
    time and accumulate the result
    """


    # interface
    def compute(self):
        """
        Invoke the evaluation routines of my descendants to compute my value
        """
        return functools.reduce(self._closure, (node.value for node in self._domain))


    ## the overriden method that performs the actual computation
    _closure = None


# end of file 
