#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#

def test():
    import math
    import pyre.units

    one = pyre.units.unit(value=1, derivation=(0,0,0,0,0,0,0))

    assert 1.0 == float(one)
    assert -1.0 == float(-one)
    assert 2.0 == float(2*one)
    assert 2.0 == float(one*2)
    assert 0.5 == float(one/2)
    assert 1.0 == float(one**2)
    assert math.exp(1) == math.exp(one)

    return

# main
if __name__ == "__main__":
    test()


# end of file 
