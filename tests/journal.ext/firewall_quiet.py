#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that we can suppress all channel output
    """
    # get the channel
    from journal.ext.journal import Firewall as firewall

    # suppress all output
    firewall.quiet()

    # make a channel
    channel = firewall(name="test.journal.firewall")
    # add some metadata
    channel.notes["time"] = "now"

    # carefully
    try:
        # inject
        channel.line("firewall:")
        channel.log("    a nasty bug was detected")
        # shouldn't get here
        assert False, "unreachable"
    # if the correct exception was raised
    except channel.FirewallError as error:
        # check the description
        assert str(error) == "test.journal.firewall: FIREWALL BREACHED!"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
