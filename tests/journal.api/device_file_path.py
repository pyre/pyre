#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that a file device reports the path to its file
    """
    # externals
    import os
    import tempfile

    # access
    import journal

    # work in a scratch area, so nothing is left behind
    with tempfile.TemporaryDirectory() as scratch:
        # the path to the file
        path = os.path.join(scratch, "device_file_path.log")
        # make a file device
        device = journal.file(path=path)
        # check its path
        assert device.path == path, device.path
        # and let go of it, so the file is closed before the scratch area is cleaned up
        del device

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
