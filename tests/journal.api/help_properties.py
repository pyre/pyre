#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify access to the channel properties
    """
    # access
    import journal

    # make a channel
    channel = journal.help("test.channel")

    # verify its name
    assert channel.name == "test.channel"
    # check that it is read-only
    try:
        # by attempting to modify
        channel.name = "foo"
        # hence, we can't get here
        assert False, "unreachable"
    # if all goes well
    except AttributeError as error:
        # no problem
        pass

    # verify its detail is at 1 by default
    assert channel.detail == 1
    # that it can be modified
    channel.detail = 5
    # and the assignment sticks
    assert channel.detail == 5

    # verify its activation state is on by default
    assert channel.active is True
    # that it can be modified
    channel.active = False
    # and the assignment sticks
    assert channel.active is False

    # verify its not fatal
    assert channel.fatal is False
    # that it can be modified
    channel.fatal = True
    # and the assignment sticks
    assert channel.fatal is True

    # verify that the accessible device is the console
    assert channel.device.name == "cout"
    # make a trash can
    trash = journal.trash()
    # register it as the device
    channel.device = trash
    # and verify that the assignment sticks
    assert channel.device is trash
    # check the name
    assert channel.device.name == "trash"
    # and verify that it's different from the default device held by the class
    assert channel.device is not channel.defaultDevice

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
