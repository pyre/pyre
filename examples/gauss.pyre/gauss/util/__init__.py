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
def counter():
    from .Counter import Counter
    return Counter()


def printer():
    from .Printer import Printer
    return Printer()


# end of file 
