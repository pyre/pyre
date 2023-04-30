#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that we can look up channel names and retrieve the associated inventory
    """
    # get the channel
    from journal.Channel import Channel

    # make a severity
    class Severity(Channel, active=True, fatal=True):
        """
        A sample derivation
        """

    # get the index
    index = Severity.index
    # look up a name
    inventory = index.lookup(name="test.index")

    # verify it is an instance of the correct class
    assert isinstance(inventory, Severity.inventory_type)
    # hence the state is on
    assert inventory.active is True
    # it is fatal
    assert inventory.fatal is True
    # and the device is null
    assert inventory.device is None

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
