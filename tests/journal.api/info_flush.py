#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


def test():
    """
    Verify that the channel buffers get flushed properly after {log}
    """
    # get the journal
    import journal

    # make a channel
    channel = journal.info(name="tests.journal.info")
    # send the output to the trash
    channel.device = journal.trash()

    # inject
    channel.log("hello world!")

    # verify that the buffer is empty after the flush
    assert len(channel.page) == 0

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
