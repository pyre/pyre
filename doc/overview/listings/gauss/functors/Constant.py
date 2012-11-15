# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre
from .Functor import Functor

class Constant(pyre.component, family="gauss.functors.constant",
               implements=Functor):
    """
    A representation of constant functions
    """

    # public state
    value = pyre.properties.float(default=1)
    value.doc = "the value of the constant functor"""

    # interface
    @pyre.export
    def eval(self, points):
        """
        Compute the value of the function
        """
        # cache the constant
        constant = self.value
        # return the constant regardless of the evaluation point
        for point in points: yield constant
        # all done
        return


# end of file 
