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
    import pyre.filesystem

    # fake a filesystem
    class filesystem: pass

    # build a node
    n = pyre.filesystem.node(filesystem=filesystem())

    # and return it
    return n


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
