#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Verify that time conversions work as  expected
"""


def test():
    import pyre.schemata

    # create a descriptor
    descriptor = pyre.schemata.time()

    # casts are not implemented yet
    magic = descriptor.coerce('13:30:00')
    # check
    assert magic.tm_hour == 13
    assert magic.tm_min == 30
    assert magic.tm_sec == 0

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
