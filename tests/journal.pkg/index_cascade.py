#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that channels lower in the hierarchy inherit the default state of their parent
    """
    # get the channel base class
    from journal.Channel import Channel

    # make a severity
    class Severity(Channel, active=True, fatal=True):
        """
        A sample derivation
        """

    # get the trash can
    from journal.Trash import Trash

    # get the index
    index = Severity.index
    # and the inventory type
    inventory_type = Severity.inventory_type

    # look up a name
    parent = index.lookup(name="test.index.parent")
    # verify it is an instance of the correct class
    assert isinstance(parent, inventory_type)
    # hence the state is on
    assert parent.active is True
    # it is fatal
    assert parent.fatal is True
    # and the device is null
    assert parent.device is None

    # deactivate it
    parent.active = False
    # make it non-fatal
    parent.fatal = False
    # and set the device to a trash can
    parent.device = Trash()

    # lookup a name that is lower in the hierarchy
    child = index.lookup(name="test.index.parent.blah.blah.child")
    # make sure it's an instance of the correct type
    assert isinstance(child, inventory_type)
    # that it's state is the same as the parent
    assert child.active == parent.active
    assert child.fatal == parent.fatal
    # and that it inherited the device correctly
    assert child.device is parent.device

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
