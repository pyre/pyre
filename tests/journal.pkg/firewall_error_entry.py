#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    The exception raised by a fatal firewall carries the entry it recorded
    """
    # get the trash can
    from journal.Trash import Trash as trash

    # and the channel
    from journal.Firewall import Firewall as firewall

    # make a channel
    channel = firewall(name="tests.journal.firewall")
    # send the output to the trash
    channel.device = trash()

    # carefully
    try:
        # inject
        channel.line("nasty bug:")
        channel.log("    hello world!", code="7")
        # shouldn't get here
        assert False, "unreachable"
    # if the correct exception was raised
    except channel.FirewallError as error:
        # check the summary
        assert str(error) == "tests.journal.firewall: FIREWALL BREACHED!"
        # the channel name
        assert error.channel == "tests.journal.firewall"
        # the page
        assert error.page == ["nasty bug:", "    hello world!"]
        # and the notes
        assert error.notes["severity"] == "firewall"
        assert error.notes["code"] == "7"
        assert error.notes["filename"] == __file__

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
