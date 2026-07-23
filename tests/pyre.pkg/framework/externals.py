#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: verify that the host carries a package database stack
"""


def test():
    """
    Verify the host description of the package database engines
    """
    import pyre

    # build the executive
    executive = pyre.executive

    # the host must describe its package database stack
    assert executive.host.packagers
    # and the fallback prober must always be part of it
    assert "bare" in executive.host.packagers

    # all done
    return executive


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
