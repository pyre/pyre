#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that a file device opened with mode {a} adds to its file rather than replacing it
    """
    # externals
    import os
    import tempfile

    # access
    import journal

    # work in a scratch area, so nothing is left behind
    with tempfile.TemporaryDirectory() as scratch:
        # the path to the file
        path = os.path.join(scratch, "device_file_append.log")
        # put something in it
        with open(path, "w") as stream:
            # a marker that should survive
            stream.write("marker\n")
        # make a channel
        channel = journal.info("tests.journal.append")
        # point it to a file device that appends
        channel.device = journal.file(path=path, mode="a")
        # record an entry
        channel.log("appended")
        # let go of the channel and its device, so the file is flushed and closed
        del channel
        # read the file
        with open(path) as stream:
            # all of it
            content = stream.read()
        # the marker is still there
        assert content.startswith("marker"), content
        # and so is the entry
        assert "appended" in content, content

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
