#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Verify that locators can be chained correctly
    """
    # get the package
    import pyre.tracking

    # make two locators
    first = pyre.tracking.simple(source="first")
    second = pyre.tracking.simple(source="second")
    # chain them together
    chain = pyre.tracking.chain(this=first, next=second)
    # verify the display
    assert str(chain) == "first, second"

    # all done
    return chain


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
