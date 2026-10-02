#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A non-fatal firewall hands back the exception it would have raised
    """
    # get the trash can
    from journal.Trash import Trash as trash

    # and the channel
    from journal.Firewall import Firewall as firewall

    # make a channel
    channel = firewall(name="tests.journal.firewall")
    # send the output to the trash
    channel.device = trash()
    # make it non-fatal
    channel.fatal = False

    # carefully
    try:
        # raise what the channel hands back
        raise channel.log("a nasty bug was detected")
    # if it is the right exception
    except channel.FirewallError:
        # all good
        pass

    # the entry was flushed after it was recorded
    assert len(channel.page) == 0

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
