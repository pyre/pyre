#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that channels lower in the hierarchy inherit the default state of their parent
    """
    # get the channel
    from journal.ext.journal import Help
    # and the trash can
    from journal.ext.journal import Trash

    # make a channel
    parent = Help(name="test.index.parent")
    # verify that the state is on
    assert parent.active is True
    # it's non-fatal
    assert parent.fatal is False
    # and the device is at the default value
    assert parent.device is Help.chronicler.device

    # activate it
    parent.active = True
    # make it fatal
    parent.fatal = True
    # and set the device to a trash can
    parent.device = Trash()

    # lookup a name that is lower in the hierarchy
    child = Help(name="test.index.parent.blah.blah.child")
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
