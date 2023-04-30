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
    import journal

    # make a channel
    ch_1 = journal.error("test.channel")
    # deactivate it
    ch_1.active = False
    # and make it non-fatal
    ch_1.fatal = False

    # make another
    ch_2 = journal.error("test.channel")
    # verify it is inactive
    assert ch_2.active == False
    # and non fatal
    assert ch_2.fatal == False
    # activate it
    ch_2.active = True
    # and make it fatal
    ch_2.fatal = True

    # verify that both channels are now inactive
    assert ch_1.active == True
    assert ch_2.active == True
    # and once again, using {__bool__}
    assert bool(ch_1) == True
    assert bool(ch_2) == True

    # verify that they are both fatal
    assert ch_1.fatal == True
    assert ch_2.fatal == True

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
