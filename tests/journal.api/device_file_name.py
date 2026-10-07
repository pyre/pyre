#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that a file device is named {file}
    """
    # externals
    import os
    import shutil

    # access
    import journal

    # the suite runs me once per implementation of the journal, possibly at the same time, so
    # each run gets its own scratch area
    implementation = "python" if os.environ.get("JOURNAL_LIBJOURNAL") == "off" else "libjournal"
    # work in a scratch area next to this driver, where the products stay for inspection
    scratch = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), f"device_file_name.{implementation}.scratch"
    )
    # start clean, by removing whatever a previous run left behind
    shutil.rmtree(scratch, ignore_errors=True)
    # and make it
    os.makedirs(scratch)
    # make a file device
    device = journal.file(path=os.path.join(scratch, "device_file_name.log"))
    # check its name
    assert device.name == "file", device.name
    # and let go of it, so the file is closed before the scratch area is cleaned up
    del device

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
