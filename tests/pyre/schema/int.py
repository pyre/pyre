#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
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
    assert 1 == descriptor.coerce(1)
    assert 1 == descriptor.coerce("1")
    # failures
    try:
        descriptor.coerce(test)
        assert False
    except descriptor.CastingError as error:
        assert str(error) == "int() argument must be a string or a number, not 'function'"
        
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
