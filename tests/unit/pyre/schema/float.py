#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Check that float conversions work as expected
"""


def test():
    import pyre.schema

    # create a descriptor
    descriptor = pyre.schema.float

    # casts
    # successful
    assert 1.2 == descriptor.cast(1.2)
    assert 1.2 == descriptor.cast("1.2")
    # failures
    try:
        descriptor.cast(test)
        assert False
    except descriptor.CastingError as error:
        assert str(error) == "float() argument must be a string or a number"
        
    return


# main
if __name__ == "__main__":
    test()


# end of file 
