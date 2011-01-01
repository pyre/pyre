#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
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
    assert True == descriptor.pyre_cast(True)
    assert True == descriptor.pyre_cast("y")
    assert True == descriptor.pyre_cast("on")
    assert True == descriptor.pyre_cast("ON")
    assert True == descriptor.pyre_cast("yes")
    assert True == descriptor.pyre_cast("YES")
    assert True == descriptor.pyre_cast("true")
    assert True == descriptor.pyre_cast("TRUE")

    assert False == descriptor.pyre_cast(False)
    assert False == descriptor.pyre_cast("n")
    assert False == descriptor.pyre_cast("off")
    assert False == descriptor.pyre_cast("OFF")
    assert False == descriptor.pyre_cast("no")
    assert False == descriptor.pyre_cast("NO")
    assert False == descriptor.pyre_cast("false")
    assert False == descriptor.pyre_cast("FALSE")

    # failures
    try:
        descriptor.pyre_cast(test)
        assert False
    except descriptor.CastingError as error:
        assert str(error) == "could not cast to bool"
        
    return


# main
if __name__ == "__main__":
    test()


# end of file 
