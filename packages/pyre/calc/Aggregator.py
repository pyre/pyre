# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Polyadic import Polyadic


class Aggregator(Polyadic):
    """
    Base class for evaluators that apply an operation on a sequence of nodes
    """


    # interface
    def compute(self):
        """
        Invoke the evaluation routines of my descendants to compute my value
        """
        return self._closure(node.value for node in self.domain)


    ## the overriden method that performs the actual computation
    _closure = None


# end of file 
