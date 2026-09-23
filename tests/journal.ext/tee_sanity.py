#!/usr/bin/env python3
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

    # the file
    path = "tee_sanity_ext.log"
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
    # inject something; the console gets a copy, and so does the file
    channel.log("hello world!")
    # let go of the tee so the file is flushed
    channel.device = journal.trash()
    del tee
    # and check that the message is in the file
    assert "hello world!" in open(path, encoding="utf-8").read()
    # clean up
    os.remove(path)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
