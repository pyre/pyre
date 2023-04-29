#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


"""
Verify that clearing the contents of filesystems destroys the nodes
"""


def test():
    # support
    import pyre.primitives
    # my package
    import pyre.filesystem

    # build a filesystem; look just deeply enough to be able to find our target, but not too
    # deeply so we don't run into trouble if the tests are running in parallel and other test
    # cases have done damage to their local filesystem
    tests = pyre.filesystem.local(root="..").discover(levels=2)
    # show me
    # print('\n'.join(tests.dump()))
    # now clear its contents explicitly
    tests.contents = {}
    # verify that all the nodes except the filesystem itself were destroyed
    assert len(tests.pyre_extent) == 1

    # all done
    return tests


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
