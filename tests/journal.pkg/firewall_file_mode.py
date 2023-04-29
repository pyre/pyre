#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Send all channel output to a log file
    """
    # get the channel
    from journal.Firewall import Firewall as firewall

    # send the output to a log file
    firewall.logfile(path="firewall_file_mode.log", mode="w")

    # make a firewall channel
    channel = firewall(name="tests.journal.firewall")
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
        # verify that the description is correct
        assert str(error) == (
            f"file='{__file__}', line='27', function='test': "
            "firewall breached; aborting..."
            )

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
