#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Check that nodes can be instantiated and that their limited interface works as advertised
"""


def test():
    # get hold of the constructor
    from pyre.filesystem.Node import Node

    # fake a filesystem
    class filesystem: pass

    # build a node
    node = Node(filesystem=filesystem())

    # count its children to verify the interface
    children = 0
    for child in node.contents:
        children += 1
    assert children == 0

    # all done
    return node


# main
if __name__ == "__main__":
    test()


# end of file 
