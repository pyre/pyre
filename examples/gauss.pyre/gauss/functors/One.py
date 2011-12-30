# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre
from .Functor import Functor


class One(pyre.component, family="gauss.functors.one", implements=Functor):
    """
    The unit function 
    """


    # interface
    @pyre.export
    def eval(self, points):
        """
        Compute the value of the function on the supplied points
        """
        # loop over the points
        for point in points:
            yield 1
        # all done
        return


# end of file 
