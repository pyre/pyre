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


    # the suggested default implementation
    @classmethod
    def default(cls):
        """
        The default implementation of the {Functor} interface
        """
        from .One import One
        return One


    # interface
    @pyre.provides
    def eval(self, points):
        """
        Evaluate the function at the supplied points
        """


# end of file 
