#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


"""
Verify that time conversions work as  expected
"""


def test():
    import pyre.schemata

    # create a descriptor
    time = pyre.schemata.time()

    # casts are not implemented yet
    magic = time.coerce('13:30:00')
    # check
    assert magic.tm_hour == 13
    assert magic.tm_min == 30
    assert magic.tm_sec == 0

    # now one with a different input format
    time = pyre.schemata.time(format='%H|%M|%S')
    # try again
    magic = time.coerce(value='13|30|00')
    # check
    assert magic.tm_hour == 13
    assert magic.tm_min == 30
    assert magic.tm_sec == 0

    # how about one
    try:
        # with the wrong format
        time.coerce(value='13-30-00')
        assert False
    # it should fail
    except time.CastingError: 
        # so no problem
        pass

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
