#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that an entry sent to a splitter reaches every device attached to it
    """
    # access
    import journal

    # for the scratch files
    import os

    # two files
    first = "splitter_fanout_pkg_first.log"
    second = "splitter_fanout_pkg_second.log"
    # a splitter over a device for each
    splitter = journal.splitter()
    splitter.attach(journal.file(path=first)).attach(journal.file(path=second))
    # make a channel
    channel = journal.info(name="tests.journal.splitter")
    # send its output to the splitter
    channel.device = splitter
    # inject something
    channel.log("hello world!")
    # let go of the splitter so the files are flushed
    channel.device = journal.trash()
    del splitter
    # both files got the message
    one = open(first, encoding="utf-8").read()
    two = open(second, encoding="utf-8").read()
    assert "hello world!" in one
    # and the same message
    assert one == two
    # clean up
    os.remove(first)
    os.remove(second)
    # all done
    return


# main
if __name__ == "__main__":
    # skip the bindings, so the pure python implementation is exercised
    journal_no_libjournal = True
    # run the test
    test()


# end of file
