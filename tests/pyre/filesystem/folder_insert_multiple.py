#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify node insertion in folders

In this test, we first create the parent of the target node separately, followed by an
insertion of the target node through its absolute path. We then check that the tree structure
is as expected
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
    # and a couple of nodes
    mga = Node(filesystem=fs)
    users = Folder(filesystem=fs)

    # add them to the folder
    root._insert(node=users, path="/home/users")
    root._insert(node=mga, path="/home/users/mga")

    # check that it was done correctly
    assert len(root.contents) == 1
    assert "home" in root.contents

    home = root.contents["home"] 
    assert len(home.contents) == 1
    assert "users" in home.contents

    users = home.contents["users"] 
    assert len(users.contents) == 1
    assert "mga" in users.contents

    assert users.contents["mga"] == mga

    # all done
    return root


# main
if __name__ == "__main__":
    test()


# end of file 
