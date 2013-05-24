#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Verify that date conversions work as  expected
"""


def test():
    import pyre.schemata

    # create a descriptor
    date = pyre.schemata.date()

    # convert a string into a date
    magic = date.coerce('1992-12-21')
    # check
    assert magic.tm_year == 1992
    assert magic.tm_mon == 12
    assert magic.tm_mday == 21

    # now one with a different input format
    date = pyre.schemata.date(format='%Y/%m/%d')
    # try again
    magic = date.coerce(value='1992/12/21')
    # check
    assert magic.tm_year == 1992
    assert magic.tm_mon == 12
    assert magic.tm_mday == 21

    # how about one
    try:
        # with the wrong format
        date.coerce(value='1992-12-21')
        assert False
    # it should fail
    except date.CastingError: 
        # so no problem
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
