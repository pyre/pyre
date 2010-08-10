#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#

def test():
    import pyre.units

    m = pyre.units.dimensional(value=1, derivation=(1,0,0,0,0,0,0))
    assert m+m == 2*m
    assert 0 == m-m
    assert m**2 == m*m

    return

# main
if __name__ == "__main__":
    test()


# version
__id__ = "$Id$"

# end of file 
