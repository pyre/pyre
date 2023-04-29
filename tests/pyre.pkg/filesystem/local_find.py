#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


"""
Verify searching through folders for named nodes
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

    # look for this file
    this = tests["filesystem/local_find.py"]
    # make sure we got it
    assert this is not None
    # and that it is the right uri
    assert this.uri == pyre.primitives.path(__file__).resolve()

    # all done
    return this


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
