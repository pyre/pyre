#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that attempts to create local filesystems with nonexistent roots fails as expected
"""


def test():
    import pyre.filesystem

    dummy = "./local_rootNotDirectory.py"
    try:
        pyre.filesystem.local(root=dummy)
        assert False
    except pyre.filesystem.MountPointError as error:
        import os
        target = os.path.abspath(dummy)
        assert str(error) == (
            "error while mounting {!r}: invalid mount point".format(target))

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
