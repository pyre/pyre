#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


def test():
    """
    Verify that channels lower in the hierarchy inherit their parent default state
    """
    # get the channel
    from journal.ext.journal import Error
    # and the trash can
    from journal.ext.journal import Trash

    # make a channel
    parent = Error(name="test.index.parent")
    # verify that the state is off
    assert parent.active is True
    # and that is fatal
    assert parent.fatal is True
    # and the device is at the default value
    assert parent.device is parent.chronicler.device

    # deactivate it
    parent.active = False
    # and make it non fatal
    parent.fatal = False
    # and set the device to a trash can
    parent.device = Trash()

    # lookup a name that is lower in the hierarchy
    child = Error(name="test.index.parent.blah.blah.child")
    # that its state is the same as the parent
    assert child.active == parent.active
    assert child.fatal == parent.fatal
    # and that it inherited the device correctly
    assert child.device is parent.device

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
