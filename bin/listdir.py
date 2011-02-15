#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Print the contents of the filesystem rooted at the current directory
"""


def listdir():
    import os
    import pyre.filesystem

    finder = pyre.filesystem.newFinder()
    cwd = pyre.filesystem.newLocalFilesystem(root=".").sync()

    me = os.path.normpath(__file__)
    for node,path in finder.explore(cwd):
        if path == me:
            continue
        print(path)

    return cwd


# main
if __name__ == "__main__":
    listdir()


# end of file 
