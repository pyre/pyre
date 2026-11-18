#!/usr/bin/env python3
# -*- python -*-
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

    # two files: one
    first = "splitter_fanout_ext_first.log"
    # and another
    second = "splitter_fanout_ext_second.log"
    # a splitter
    splitter = journal.splitter()
    # over a device for each
    splitter.attach(journal.file(path=first)).attach(journal.file(path=second))
    # make a channel
    channel = journal.info(name="tests.journal.splitter")
    # send its output to the splitter
    channel.device = splitter
    # inject something
    channel.log("hello world!")
    # detach the splitter from the channel
    channel.device = journal.trash()
    # and let go of it, so the files are flushed
    del splitter
    # read the first file
    with open(first, encoding="utf-8") as stream:
        # all of it
        one = stream.read()
    # and the second
    with open(second, encoding="utf-8") as stream:
        # all of it
        two = stream.read()
    # both files got the message
    assert "hello world!" in one
    # and the same message
    assert one == two
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
