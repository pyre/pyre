# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre
from .Functor import Functor


class Constant(pyre.component, family="gauss.functors.constant", implements=Functor):
    """
    Component that implements a constant function
    """

    # public state
    value = pyre.components.float(default=1)
    value.doc = "the value of the function"


    @pyre.components.export
    def eval(self, points):
        """
        Compute the value of the function
        """
        # cache the value
        value = self.value
        # the evaluation loop
        for point in points:
            yield value
        # all done
        return


# end of file 
