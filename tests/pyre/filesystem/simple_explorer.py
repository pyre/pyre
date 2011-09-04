#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise the simple filesystem explorer
"""


def test():
    import pyre.filesystem

    # make a filesystem
    fs = pyre.filesystem.newVirtualFilesystem()
    # create a couple of nodes and insert them into the filesystem
    fs["/home/users/mga/dv/tools/bin/hello"] = fs.newNode()
    fs["/home/users/mga/dv/tools/lib/libhello.a"] = fs.newNode()

    # explore
    explorer = pyre.filesystem.newSimpleExplorer()
    contents = explorer.explore(fs)
    
    # check
    assert contents == [
        "(d) /",
        "  (d) home",
        "    (d) users",
        "      (d) mga",
        "        (d) dv",
        "          (d) tools",
        "            (d) bin",
        "              (f) hello",
        "            (d) lib",
        "              (f) libhello.a",
        ]

    return fs, explorer


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
