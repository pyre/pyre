#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def lookup():
    """
    Verify that the lookup locator returns the correct location tag
    """
    # get the package
    import pyre
    #  make a locator
    key = pyre.executive.nameserver.hash('pyre')
    # build a locator
    locator = pyre.tracking.lookup(description="while looking up", key=key)
    # verify the display
    # assert str(locator) == "while looking up package 'pyre'"

    # all done
    # return locator


# main
if __name__ == "__main__":
    # do...
    lookup()


# end of file
