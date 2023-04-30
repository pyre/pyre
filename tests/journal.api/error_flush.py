#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that the channel buffers are cleared after flushing a message; this is a non-trivial
    test because it guarantees that the implementation handles the transaction correctly
    """
    # get the journal
    import journal

    # make a channel
    channel = journal.error(name="test.journal.error")
    # send the output to the trash
    channel.device = journal.trash()

    # carefully
    try:
        # inject
        channel.log("hello world!")
        # shouldn't get here
        assert False, "unreachable"
    # if the correct exception was raised
    except channel.ApplicationError as error:
        # no problem
        pass

    # verify that the buffer is empty after the flush
    assert len(channel.page) == 0

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
