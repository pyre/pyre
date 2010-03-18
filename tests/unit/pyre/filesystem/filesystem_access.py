#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: verify that we can create filesystem instances
"""


def test():
    from pyre.filesystem.Filesystem import Filesystem

    # create a filesystem
    fs =  Filesystem()

    # create a folder a few levels down from the root
    mpath = "/home/users/mga"
    mga = fs.newFolder()
    fs.insert(node=mga, path=mpath)
    # check that we can retrieve it
    assert mga == fs[mpath]

    # now add a subfolder
    tpath = '/dv/tools'
    tools = fs.newFolder()
    fs.insert(node=tools, path=mpath + tpath)

    # and retrieve it
    assert fs[mpath+tpath] == mga[tpath]
    
    return fs


# main
if __name__ == "__main__":
    import pyre.filesystem
    # adjust the package metaclasses
    from pyre.patterns.ExtentAware import ExtentAware
    pyre.filesystem._metaclass_Node = ExtentAware
    pyre.filesystem._metaclass_Filesystem = ExtentAware

    test()

    # check that the filesystem was destroyed
    from pyre.filesystem.Filesystem import Filesystem
    # print("Filesystem extent:", len(Filesystem._pyre_extent))
    assert len(Filesystem._pyre_extent) == 0

    # now check that the nodes were all destroyed
    from pyre.filesystem.Node import Node
    # print("VNode extent:", len(VNode._pyre_extent))
    assert len(Node._pyre_extent) == 0


# end of file 
