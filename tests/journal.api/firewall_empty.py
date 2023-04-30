#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that empty messages are handled correctly
    """
    # get the journal
    import journal

    # make a channel
    channel = journal.firewall(name="test.journal.firewall")

    # carefully
    try:
        # inject an empty message
        channel.log()
        # shouldn't get here
        assert False, "unreachable"
    # if the correct exception was raised
    except channel.FirewallError as error:
        # all good
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
