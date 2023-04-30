#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify we can make firewalls non-fatal
    """
    # get the journal
    import journal

    # make a firewall channel
    channel = journal.firewall(name="tests.journal.firewall")
    # make it non-fatal
    channel.fatal = False
    # send the output to the trash
    channel.device = journal.trash()
    # add some metadata
    channel.notes["time"] = "now"

    # carefully
    try:
        # inject
        channel.line("firewall:")
        channel.log("    a nasty bug was detected")
    # if the correct exception was raised
    except channel.FirewallError as error:
        # shouldn't get here
        assert False, "unreachable"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
