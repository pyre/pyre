#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify creation of filesystems based on zipfiles
"""


def test():
    import pyre.filesystem

    # NYI: replace this with (a dunamically generated) pyre-1.0.zip
    home = pyre.filesystem.newZipFilesystem(root="/Users/mga/tmp/pyre-1.0.zip")
    home._dump(interactive=False) # change to True to see the dump

    return home


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
    # print("Node extent:", len(Node._pyre_extent))
    assert len(Node._pyre_extent) == 0


# end of file 
