#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Check that array conversions work as expected
"""


def test():
    import pyre.schema

    # create a descriptor
    descriptor = pyre.schema.array

    # casts
    # successful
    assert () == descriptor.pyre_cast([])
    assert (1.,) == descriptor.pyre_cast([1])
    assert (1., 2.) == descriptor.pyre_cast([1,2])
    assert () == descriptor.pyre_cast("[]")
    assert () == descriptor.pyre_cast("()")
    assert () == descriptor.pyre_cast("{}")
    assert (1.,) == descriptor.pyre_cast("[1]")
    assert (1.,) == descriptor.pyre_cast("{1}")
    assert (1.,) == descriptor.pyre_cast("(1,)")
    assert (1., 2.) == descriptor.pyre_cast("[1, 2]")
    assert (1., 2.) == descriptor.pyre_cast("{1, 2}")
    assert (1., 2.) == descriptor.pyre_cast("(1, 2)")
    # failures
    try:
        descriptor.pyre_cast(test)
        assert False
    except descriptor.CastingError as error:
        pass
        
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
