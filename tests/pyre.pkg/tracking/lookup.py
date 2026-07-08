#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the lookup locator returns the correct location tag
"""


def lookup():
    import pyre

    key = pyre.executive.nameserver.hash("pyre")
    locator = pyre.tracking.lookup(description="while looking up", key=key)

    assert str(locator) == "while looking up package 'pyre'"

    return locator


# main
if __name__ == "__main__":
    # do...
    lookup()


# end of file
