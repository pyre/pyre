#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Check that array conversions work as expected
"""


def test():
    import pyre.schema

    # create a descriptor
    descriptor = pyre.schema.tuple

    # casts
    # successful
    assert () == descriptor.pyre_cast(())
    assert () == descriptor.pyre_cast([])
    assert () == descriptor.pyre_cast("()")
    assert () == descriptor.pyre_cast("[]")

    assert ("one",) == descriptor.pyre_cast(("one",))
    assert ("one",) == descriptor.pyre_cast(["one"])
    assert ("one",) == descriptor.pyre_cast("[one]")
    assert ("one",) == descriptor.pyre_cast("(one)")

    assert ("one", "two") == descriptor.pyre_cast(("one", "two"))
    assert ("one", "two") == descriptor.pyre_cast(["one", "two"])
    assert ("one", "two") == descriptor.pyre_cast("(one,two)")
    assert ("one", "two") == descriptor.pyre_cast("[one,two]")
    assert ("one", "two") == descriptor.pyre_cast("(one, two)")
    assert ("one", "two") == descriptor.pyre_cast("[one, two]")

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
