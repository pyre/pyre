#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify node insertion in folders
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
    root._insert(path="/home/users/mga", node=mga)

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
