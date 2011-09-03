#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise node algebra
"""

# get the package
import pyre.algebraic
    

def test():

    # declare a couple of nodes
    zero = pyre.algebraic.var(value=0)
    one = pyre.algebraic.var(value=1)

    # and
    assert ((zero == 0) & (one == 1)).value == True

    # or
    assert ((zero == 0) | (zero == one)).value == True
    assert ((zero == one) | (zero == 0)).value == True

    return one, zero


# main
if __name__ == "__main__":
    test()


# end of file 
