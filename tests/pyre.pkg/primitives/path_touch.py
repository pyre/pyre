#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a path creates its file, refreshes the times of an existing one, and refuses to
touch an existing file when told so; the file {path_touch.txt} is the product of the test
"""

# externals
import os
import stat

# support
import pyre


def test():
    """
    Touch a file, then touch it again, with and without permission to find it there
    """
    # the file
    path = pyre.primitives.path("path_touch.txt")
    # start from scratch, in case a previous run left it behind
    if path.exists():
        # by removing it
        path.unlink()

    # the umask filters the permissions; reading it means setting it
    umask = os.umask(0)
    # so put it right back
    os.umask(umask)
    # touch the path
    path.touch()
    # the file is there, and it's a regular one
    assert path.isFile()
    # with the default permissions, as filtered by the umask
    assert stat.S_IMODE(path.stat().st_mode) == 0o666 & ~umask

    # an hour before the file was made
    past = path.stat().st_mtime - 3600
    # is where its times go
    os.utime(path, (past, past))
    # touch it again
    path.touch()
    # and check that it has been marked as modified since
    assert path.stat().st_mtime > past

    # touching it when it must not exist
    try:
        # should fail
        path.touch(exist_ok=False)
        # so we shouldn't get here
        assert False, "unreachable"
    # by complaining that it exists
    except FileExistsError:
        # which is what we expect
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
