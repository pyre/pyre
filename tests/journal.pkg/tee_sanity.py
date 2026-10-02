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

    # for the scratch file
    import os

    # to capture the console
    import io
    import sys

    # the file
    path = "tee_sanity_pkg.log"
    # capture the console, which binds the standard output when it is built
    console, sys.stdout = sys.stdout, io.StringIO()
    # carefully
    try:
        # make a tee over the console and the file
        tee = journal.tee(paths=[path])
    # in any case
    finally:
        # grab the capture
        capture = sys.stdout
        # and restore the standard output
        sys.stdout = console
    # check its name
    assert tee.name == "tee"
    # it holds the console and the file
    assert len(tee.outputs) == 2
    # make a channel
    channel = journal.info(name="tests.journal.tee")
    # send its output to the tee
    channel.device = tee
    # inject something; the console gets a copy, and so does the file
    channel.log("hello world!")
    # let go of the tee so the file is flushed
    channel.device = journal.trash()
    del tee
    # check that the message made it to the console
    assert "hello world!" in capture.getvalue()
    # and to the file
    assert "hello world!" in open(path, encoding="utf-8").read()
    # clean up
    os.remove(path)
    # all done
    return


# main
if __name__ == "__main__":
    # skip the bindings, so the pure python implementation is exercised
    journal_no_libjournal = True
    # run the test
    test()


# end of file
