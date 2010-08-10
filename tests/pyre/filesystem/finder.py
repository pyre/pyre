#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
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
    finder = pyre.filesystem.newFinder()
    contents = [ path for node,path in finder.explore(fs) ]
    
    # check
    assert contents == [
        "home",
        "home/users",
        "home/users/mga",
        "home/users/mga/dv",
        "home/users/mga/dv/tools",
        "home/users/mga/dv/tools/bin",
        "home/users/mga/dv/tools/bin/hello",
        "home/users/mga/dv/tools/lib",
        "home/users/mga/dv/tools/lib/libhello.a",
        ]

    return fs, finder


# main
if __name__ == "__main__":
    test()


# end of file 
