# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# access to the framework
import pyre


# declaration
class Functor(pyre.protocol, family="gauss.functors"):
    """
    Protocol declarator for function objects
    """


    # the suggested default implementation
    @classmethod
    def pyre_default(cls):
        """
        The default implementation of the {Functor} protocol
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
