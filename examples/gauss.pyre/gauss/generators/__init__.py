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
def wickmannhill(name=None):
    from .WichmannHill import WichmannHill

    # if a name was given, instantiate and return
    if name:
        return WichmannHill(name=name)
    
    # otherwise, return the class record
    return WichmannHill


# end of file 
