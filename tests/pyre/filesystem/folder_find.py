#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify searching through folders for named nodes
"""


def test():
    from pyre.filesystem.Node import Node
    from pyre.filesystem.Folder import Folder

    # fake a filesystem
    class filesystem: pass
    # build a fake filesystem
    fs = filesystem()

    # build a folder
    root = Folder(filesystem=fs)
    # and a node
    mga = Node(fs)

    # add it to the folder
    root._insert(path="home/users/mga", node=mga)

    # now retrieve it
    target = root._find("/home/users/mga")
   
    # make sure it is the same node
    assert mga == target

    # all done
    return root


# main
if __name__ == "__main__":
    test()


# end of file 
