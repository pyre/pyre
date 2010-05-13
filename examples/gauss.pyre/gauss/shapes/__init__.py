# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Package that contains the component declarations
"""

# factories
def ball(name=None):
    from .Ball import Ball

    # if a name was given, instantiate and return
    if name:
        return Ball(name=name)
    
    # otherwise, return the class record
    return Ball


def box(name=None):
    from .Box import Box

    # if a name was given, instantiate and return
    if name:
        return Box(name=name)
    
    # otherwise, return the class record
    return Box


# end of file 
