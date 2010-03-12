# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Aggregator import Aggregator


class Maximum(Aggregator):
    """
    Compute the maximum of the nodes in my domain
    """


    ## the overriden method that performs the actual computation
    _closure = max


# end of file 
