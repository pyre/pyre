#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that node insertion fails when an intermediate path component is not a folder
"""


def test():
    from pyre.filesystem import FolderError
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
    root.insert(path="/home/users/mga", node=mga)
    # now create another node
    tmp = Node(fs)
    # and attempt to add it to mga
    try:
        root.insert(path="/home/users/mga/tmp", node=tmp)
        assert False
    except FolderError as error:
        assert (
            error.message == "error while inserting '/home/users/mga/tmp': 'mga' is not a folder")

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file 
