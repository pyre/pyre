#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
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
    test()


# end of file 
