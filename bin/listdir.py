#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


"""
Print the contents of the filesystem rooted at the current directory
"""


def listdir():
    import os
    import pyre.filesystem

    explorer = pyre.filesystem.treeExplorer()
    cwd = pyre.filesystem.local(root='.').discover()

    me = os.path.normpath(__file__)
    for line in explorer.explore(node=cwd, label='.'):
        print(line)

    return cwd


# main
if __name__ == "__main__":
    listdir()


# end of file
