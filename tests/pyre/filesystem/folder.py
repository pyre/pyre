#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Check that folders can be instantiated and that their limited interface works as advertised
"""


def test():
    from pyre.filesystem.Node import Node
    from pyre.filesystem.Folder import Folder

    # fake a filesystem
    class filesystem: pass
    # build a fake filesystem
    fs = filesystem()

    # build a folder
    folder = Folder(filesystem=fs)
    # and some nodes
    usr = Node(fs)
    tmp = Node(fs)
    home = Node(fs)
    # add them to the folder
    folder.contents["usr"] = usr
    folder.contents["tmp"] = tmp
    folder.contents["home"] = home

    # count the children
    children = 0
    for child in folder.contents:
        children += 1
    assert children == 3

    # access the individual nodes
    assert usr == folder.contents["usr"]
    assert tmp == folder.contents["tmp"]
    assert home == folder.contents["home"]

    # all done
    return folder


# main
if __name__ == "__main__":
    test()


# end of file 
