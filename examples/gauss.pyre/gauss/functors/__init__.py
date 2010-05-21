# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Package that contains the functor declarations
"""

# functors
def constant(name=None):
    from .Constant import Constant

    # if a name was given, instantiate and return
    if name:
        return Constant(name=name)
    
    # otherwise, return the class record
    return Constant


def gaussian(name=None):
    from .Gaussian import Gaussian

    # if a name was given, instantiate and return
    if name:
        return Gaussian(name=name)
    
    # otherwise, return the class record
    return Gaussian


def one(name=None):
    from .One import One

    # if a name was given, instantiate and return
    if name:
        return One(name=name)
    
    # otherwise, return the class record
    return One


# end of file 
