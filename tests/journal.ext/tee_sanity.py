#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that a tee writes to the console and to its files
    """
    # access
    import journal

    # for the scratch files
    import os

    # to flush the C standard output
    import ctypes

    # the file
    path = "tee_sanity_ext.log"
    # and the capture of the console
    capture = "tee_sanity_ext.out"
    # make a tee over the console and the file
    tee = journal.tee(paths=[path])
    # check its name
    assert tee.name == "tee"
    # it holds the console and the file
    assert len(tee.outputs) == 2
    # make a channel
    channel = journal.info(name="tests.journal.tee")
    # send its output to the tee
    channel.device = tee
    # set the standard output aside
    stdout = os.dup(1)
    # open the capture
    with open(capture, mode="w") as out:
        # route the standard output to it
        os.dup2(out.fileno(), 1)
        # carefully
        try:
            # inject something; the console gets a copy, and so does the file
            channel.log("hello world!")
            # push the console copy out of the C buffers
            ctypes.CDLL(None).fflush(None)
        # in any case
        finally:
            # restore the standard output
            os.dup2(stdout, 1)
            # and release the spare descriptor
            os.close(stdout)
    # detach the tee from the channel
    channel.device = journal.trash()
    # and let go of it, so the file is flushed
    del tee
    # read what reached the console
    with open(capture, encoding="utf-8") as stream:
        # check that the message made it there
        assert "hello world!" in stream.read()
    # and what reached the file
    with open(path, encoding="utf-8") as stream:
        # check that the message made it there too
        assert "hello world!" in stream.read()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
