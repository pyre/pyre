# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre
from pyre.components.Component import Component
from ..interfaces.Functor import Functor


class Constant(Component, family="gauss.functors.constant", implements=Functor):
    """
    Component that implements a constant function
    """

    # public state
    value = pyre.components.float()
    value.doc = "the value of the function"
    value.default = 1.0


    @pyre.components.export
    def eval(self, points):
        """
        Compute the value of the function: return 1
        """
        # cache the value
        value = self.value
        # the evaluation loop
        for point in points:
            yield value
        # all done
        return


# end of file 
