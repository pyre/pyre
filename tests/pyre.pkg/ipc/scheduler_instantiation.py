#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: verify that schedulers can be instantiated
"""


def test():
    # access the package
    import pyre.ipc

    # instantiate a scheduler
    s = pyre.ipc.scheduler()
    # and return it
    return s


# main
if __name__ == "__main__":
    test()


# end of file
