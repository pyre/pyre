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
def montecarlo(name=None):
    from .MonteCarlo import MonteCarlo

    # if a name was given, instantiate and return
    if name:
        return MonteCarlo(name=name)
    
    # otherwise, return the class record
    return MonteCarlo


# end of file 
