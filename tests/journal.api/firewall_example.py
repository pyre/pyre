#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Exercise the common use case
    """
    # get the journal
    import journal

    # make a channel
    channel = journal.firewall(name="test.journal.firewall")
    # send the output to the trash
    channel.device = journal.trash()
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
