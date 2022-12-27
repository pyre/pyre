#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


"""
Create and dump a local filesystem
"""


def test():
    # externals
    import os
    # get the package
    import pyre.filesystem

    # find something stable to look at
    root = os.path.dirname(pyre.__file__)
    # mount a filesystem there and explore
    home = pyre.filesystem.local(root=root).discover(levels=2)
    # print('\n'.join(home.dump()))

    # all done
    return home


# main
if __name__ == "__main__":
    # request debugging support for the pyre.calc package
    pyre_debug = { "pyre.filesystem" }
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()

    # check that the nodes were all destroyed
    from pyre.filesystem.Node import Node
    # print("Node extent:", len(Node.pyre_extent))
    assert len(Node.pyre_extent) == 0


# end of file
