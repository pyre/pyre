#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Check that dimensional conversions work as expected
"""


def test():
    import pyre.schema
    from pyre.units.SI import m, kg, s

    # create a descriptor
    descriptor = pyre.schema.dimensional

    # casts
    # successful
    assert m == descriptor.pyre_cast("meter")
    assert 9.81*kg*m/s**2 == descriptor.pyre_cast("9.81*kg*m/s**2")

    # failures
    try:
        descriptor.pyre_cast(1)
        assert False
    except descriptor.CastingError as error:
        assert str(error) == "could not convert 1 into a dimensional quantity"
        
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
