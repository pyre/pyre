#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that channels with the same name have common state
    """
    # access
    from journal import libjournal

    # make a channel
    ch_1 = libjournal.Debug("test.channel")
    # activate it
    ch_1.active = True
    # and make it fatal
    ch_1.fatal = True

    # make another
    ch_2 = libjournal.Debug("test.channel")
    # verify it is active
    assert ch_2.active is True
    # and fatal
    assert ch_2.fatal is True
    # deactivate it
    ch_2.active = False
    # and make it non-fatal
    ch_2.fatal = False

    # verify that both channels are now inactive
    assert ch_1.active is False
    assert ch_2.active is False
    # and once again, using {__bool__}
    assert bool(ch_1) is False
    assert bool(ch_2) is False

    # verify that they are both non-fatal
    assert ch_1.fatal is False
    assert ch_2.fatal is False

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
