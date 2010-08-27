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
    fs[mpath] = mga
    # check that we can retrieve it
    assert mga == fs[mpath]

    # add a subfolder
    tpath = '/dv/tools'
    tools = fs.newFolder()
    fs[mpath + tpath] = tools

    # and retrieve it
    assert fs[mpath+tpath] == mga[tpath]

    # add a node
    hello = fs.newNode()
    tools["hello.py"] = hello

    # dump the contents
    fs._dump(interactive=False) # switch to True to see the dump
    
    return fs


# main
if __name__ == "__main__":
    # request debugging support for the pyre.calc package
    pyre_debug = { "pyre.filesystem" }

    test()

    # destroy pyre.fileserver so it doesn't confuse the extent
    import pyre
    pyre.executive.fileserver = None

    # check that the filesystem was destroyed
    from pyre.filesystem.Filesystem import Filesystem
    # print("Filesystem extent:", len(Filesystem._pyre_extent))
    assert len(Filesystem._pyre_extent) == 0

    # now check that the nodes were all destroyed
    from pyre.filesystem.Node import Node
    # print("Node extent:", len(Node._pyre_extent))
    assert len(Node._pyre_extent) == 0


# end of file 
