#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: the package is accessible
"""


def test():
    """
    Import the package and check what it publishes
    """
    # support
    import pyre.platforms.binaries

    # the readers must be there
    assert pyre.platforms.binaries.elf is not None
    assert pyre.platforms.binaries.macho is not None
    # along with the base they share
    assert pyre.platforms.binaries.image is not None
    # and the factory that picks among them
    assert pyre.platforms.binaries.read is not None

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
