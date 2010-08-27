#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Check that int conversions work as expected
"""


def test():
    import pyre.schema

    # create a descriptor
    descriptor = pyre.schema.int

    # casts
    # successful
    assert 1 == descriptor.pyre_cast(1)
    assert 1 == descriptor.pyre_cast("1")
    # failures
    try:
        descriptor.pyre_cast(test)
        assert False
    except descriptor.CastingError as error:
        assert str(error) == "int() argument must be a string or a number, not 'function'"
        
    return


# main
if __name__ == "__main__":
    test()


# end of file 
