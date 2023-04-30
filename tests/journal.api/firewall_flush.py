#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that flushing clears the message buffers
    """
    # get the journal
    import journal

    # make a channel
    channel = journal.firewall(name="test.journal.firewall")
    # send the output to the trash
    channel.device = journal.trash()

    # carefully
    try:
        # inject
        channel.log("hello world!")
        # shouldn't get here
        assert False, "unreachable"
    # if the correct exception was raised
    except channel.FirewallError as error:
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
