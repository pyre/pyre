#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# verify that the default channel state is as expected
def test():
    """
    Exercise the default channel state
    """
    # get the package
    from journal.Channel import Channel

    # derive a severity
    class Severity(Channel, active=False):
        """
        A sample derivation
        """

    # make one
    channel = Severity(name="test.channel")

    # get its inventory
    inventory = channel.inventory
    # verify that it is disabled, as we specified
    assert inventory.active == False
    # and that it is non-fatal, by default
    assert inventory.fatal == False
    # and that it has no registered device
    assert inventory.device == None

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
