#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Check that boolean conversions work as expected
"""


def test():
    import pyre.schema

    # create a descriptor
    descriptor = pyre.schema.bool

    # casts
    # successful
    assert True == descriptor.cast(True)
    assert True == descriptor.cast("y")
    assert True == descriptor.cast("on")
    assert True == descriptor.cast("ON")
    assert True == descriptor.cast("yes")
    assert True == descriptor.cast("YES")
    assert True == descriptor.cast("true")
    assert True == descriptor.cast("TRUE")

    assert False == descriptor.cast(False)
    assert False == descriptor.cast("n")
    assert False == descriptor.cast("off")
    assert False == descriptor.cast("OFF")
    assert False == descriptor.cast("no")
    assert False == descriptor.cast("NO")
    assert False == descriptor.cast("false")
    assert False == descriptor.cast("FALSE")

    # failures
    try:
        descriptor.cast(test)
        assert False
    except descriptor.CastingError as error:
        assert str(error) == "could not cast to bool"
        
    return


# main
if __name__ == "__main__":
    test()


# end of file 
