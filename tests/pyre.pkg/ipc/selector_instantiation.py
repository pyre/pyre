#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: verify that the selector foundry is callable
"""


def test():
    # access the package
    import pyre.ipc

    # call the foundry
    s = pyre.ipc.selector()
    # and hand off the class it provided
    return s


# main
if __name__ == "__main__":
    test()


# end of file
