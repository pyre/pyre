# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import pyre


class Functor(pyre.interface, family="gauss.functors"):
    """
    Interface declarator for function objects
    """


    # interface
    @pyre.provides
    def eval(self, points):
        """
        Evaluate the function at the supplied points
        """


# end of file 
