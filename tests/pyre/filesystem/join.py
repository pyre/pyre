#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    import pyre.filesystem

    # check that a pair of names can be joined correctly
    paths = ["a", "b"]
    assert pyre.filesystem.join(*paths) == pyre.filesystem.PATH_SEPARATOR.join(paths)

    # a few more
    paths = ["a", "b", "c", "d"]
    assert pyre.filesystem.join(*paths) == pyre.filesystem.PATH_SEPARATOR.join(paths)

    # check that absolute paths discard previous fragments
    paths = ["a", "b", "/c", "d"]
    assert pyre.filesystem.join(*paths) == pyre.filesystem.PATH_SEPARATOR.join(["/c", "d"])

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
