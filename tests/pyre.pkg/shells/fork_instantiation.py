#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Instantiate a script
"""


def test():
    # access the package
    import pyre

    # build a fork and return it
    return pyre.shells.fork()(name="test")


# main
if __name__ == "__main__":
    test()


# end of file
