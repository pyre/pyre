#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that message injection is handled properly
    """
    # get the trash can
    from journal.Trash import Trash as trash
    # and the channel
    from journal.Firewall import Firewall as firewall

    # make a firewall channel
    channel = firewall(name="tests.journal.firewall")
    # send the output to trash
    channel.device = trash()
    # make the firewall non-fatal
    channel.fatal = False

    # inject
    channel.log("hello world!")

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
