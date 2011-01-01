# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Reductor import Reductor


class Product(Reductor):
    """
    Compute the product of the nodes in my domain
    """


    ## the overriden method that performs the actual computation
    import operator
    _closure = operator.mul


# end of file 
