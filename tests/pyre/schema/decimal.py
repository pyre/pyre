#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that decimal conversions work as  expected
"""


def test():
    import pyre.schema

    # create a descriptor
    descriptor = pyre.schema.decimal

    # casts are not implemented yet
    try:
        descriptor.pyre_cast(None)
    except NotImplementedError:
        pass

    return


# main
if __name__ == "__main__":
    test()


# end of file 
