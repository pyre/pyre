# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Aggregator import Aggregator


class Minimum(Aggregator):
    """
    Compute the minimum of the nodes in my domain
    """


    ## the overriden method that performs the actual computation
    _closure = min


# end of file 
