#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that attempts to create local filesystems with nonexistent roots fails as expected
"""


def test():
    import pyre.filesystem

    dummy = "./local_rootNotDirectory.py"
    try:
        pyre.filesystem.newLocalFilesystem(root=dummy)
        assert False
    except pyre.filesystem.MountPointError as error:
        import os
        target = os.path.abspath(dummy)
        assert str(error) == (
            "error while mounting {0!r}: invalid mount point".format(target))

    return


# main
if __name__ == "__main__":
    test()


# end of file 
