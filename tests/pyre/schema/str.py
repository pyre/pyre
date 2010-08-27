#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that string conversions work as  expected
"""


def test():
    import pyre.schema

    # create a descriptor
    descriptor = pyre.schema.str

    # casts
    assert "hello" == descriptor.pyre_cast("hello")

    return


# main
if __name__ == "__main__":
    test()


# end of file 
