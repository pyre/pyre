#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


"""
Sanity check: exercise the utility {join} 
"""


def test():
    import pyre.filesystem

    # check that a pair of names can be joined correctly
    paths = ["a", "b"]
    assert pyre.filesystem.join(*paths) == pyre.filesystem.separator.join(paths)

    # a few more
    paths = ["a", "b", "c", "d"]
    assert pyre.filesystem.join(*paths) == pyre.filesystem.separator.join(paths)

    # check that absolute paths discard previous fragments
    paths = ["a", "b", "/c", "d"]
    assert pyre.filesystem.join(*paths) == pyre.filesystem.separator.join(["/c", "d"])

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
