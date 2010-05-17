# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Package that contains the declarations of the random number generators
"""

# factories
def mersenne(name=None):
    from .MersenneTwister import MersenneTwister

    # if a name was given, instantiate and return
    if name:
        return MersenneTwister(name=name)
    
    # otherwise, return the class record
    return MersenneTwister


# end of file 
