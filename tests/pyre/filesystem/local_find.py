#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify searching through folders for named nodes
"""


def test():
    import os
    import pyre.filesystem
    # build a filesystem
    tests = pyre.filesystem.local(root="..").discover()
    # look for this file
    this = tests["filesystem/local_find.py"]
    # make sure we got it
    assert this is not None
    # and that it is the right uri
    assert this.uri == os.path.abspath(__file__)
    # all done
    return this


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
