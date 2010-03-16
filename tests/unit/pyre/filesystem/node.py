#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    from pyre.filesystem.Node import Node

    # fake a filesystem
    class filesystem: pass

    # build a naked one
    node = Node(filesystem())

    # count its children to verify the interface
    children = 0
    for child in node.children:
        children += 1
    assert children == 0

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file 
