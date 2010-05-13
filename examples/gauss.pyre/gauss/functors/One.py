# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre
from pyre.components.Component import Component
from ..interfaces.Functor import Functor


class One(Component, family="gauss.functors.one", implements=Functor):
    """
    Component that implements the unit function
    """

    @pyre.components.export
    def eval(self, points):
        """
        Compute the value of the function: return 1
        """

        for point in points:
            yield 1.0

        return


# end of file 
