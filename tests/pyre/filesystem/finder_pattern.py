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
    fs["/home/users/mga/dv/tools/src/hello.c"] = fs.newNode()
    fs["/home/users/mga/dv/tools/src/hello.h"] = fs.newNode()
    fs["/home/users/mga/dv/tools/lib/libhello.a"] = fs.newNode()
    
    # dump the contents
    fs.dump(False) # switch to True to see the dump

    # explore
    finder = pyre.filesystem.newFinder()
    contents = [ path for node, path in finder.explore(folder=fs, pattern=r".*\.h")]
    
    # check
    assert contents == [
        "home/users/mga/dv/tools/src/hello.h",
        ]

    return fs, finder


# main
if __name__ == "__main__":
    test()


# end of file 
