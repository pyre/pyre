# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre

class Functor(pyre.interface, family="gauss.functors"):
    """
    The abstract base class for function objects
    """

    # the default implementation
    @classmethod
    def default(cls):
        """
        The default {Functor} implementation
        """
        from .Constant import Constant
        return Constant

    # required interface
    @pyre.provides
    def eval(self, points):
        """
        Evaluate the function at the supplied points
        """


# end of file 
