#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: verify that the PSL selector foundry is accessible
"""


def test():
    # access the package
    import pyre.ipc

    # invoke the psl foundry
    s = pyre.ipc.psl()

    # and hand off the class it provided
    return s


# main
if __name__ == "__main__":
    test()


# end of file
