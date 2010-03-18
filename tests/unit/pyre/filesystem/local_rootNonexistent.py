#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that attempts to create local filesystems with nonexistent roots fails as expected
"""


def test():
    import pyre.filesystem

    try:
        pyre.filesystem.newLocalFilesystem(root="/@")
        assert False
    except pyre.filesystem.MountPointError as error:
        assert str(error) == "error while mounting '/@': mount point not found"

    return


# main
if __name__ == "__main__":
    test()


# end of file 
