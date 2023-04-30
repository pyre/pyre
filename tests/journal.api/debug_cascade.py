#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that channels lower in the hierarchy inherit their parent default state
    """
    # get the journal
    import journal

    # make a channel
    parent = journal.debug(name="test.index.parent")
    # verify that the state is off
    assert parent.active is False
    # and that is not fatal
    assert parent.fatal is False
    # and the device is at the default value
    assert parent.device is parent.chronicler.device

    # activate it
    parent.active = True
    # and make it fatal
    parent.fatal = True
    # and set the device to a trash can
    parent.device = journal.trash()

    # lookup a name that is lower in the hierarchy
    child = journal.debug(name="test.index.parent.blah.blah.child")
    # that it's active is the same as the parent
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
