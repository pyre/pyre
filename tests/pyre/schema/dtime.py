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
    import pyre.schema

    # create a descriptor
    descriptor = pyre.schema.time

    # casts are not implemented yet
    try:
        descriptor.coerce(None)
    except NotImplementedError:
        pass

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
