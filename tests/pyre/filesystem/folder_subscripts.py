#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify node access in folders using the subscript notation
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
    root["/home/users/mga"] = mga

    # check that it was done correctly
    assert len(root.contents) == 1
    assert "home" in root.contents

    home = root["home"] 
    assert len(home.contents) == 1
    assert "users" in home.contents

    users = home["users"] 
    assert len(users.contents) == 1
    assert "mga" in users.contents

    assert users["mga"] == mga

    # now look for it and make sure we got the same node
    assert root["/home/users/mga"] == mga

    # all done
    return root


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
