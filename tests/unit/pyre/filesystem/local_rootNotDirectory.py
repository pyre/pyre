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
        fs = pyre.filesystem.newLocalFilesystem(root="./local_rootNotDirectory.py")
        assert False
    except pyre.filesystem.MountPointError:
        # no good way to check the error message since '.' could be anywhere
        pass

    return


# main
if __name__ == "__main__":
    test()


# end of file 
