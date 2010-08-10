#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify searching through folders for named nodes
"""


def test():
    import pyre.filesystem
    # build a filesystem
    home = pyre.filesystem.newLocalFilesystem(root="..")
    # look for this file
    this = home["filesystem/local_find.py"]
    # make sure we got it
    assert this is not None
    # all done
    return this


# main
if __name__ == "__main__":
    test()


# end of file 
