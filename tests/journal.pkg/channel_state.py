#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# channel state
def test():
    """
    Exercise the channel state
    """
    # get the channel base class
    from journal.Channel import Channel

    # make one
    d1 = Channel(name="test.channel")
    # verify the name was recorder correctly
    assert d1.name == "test.channel"
    # that its detail is set to the default value
    assert d1.detail == Channel.detail
    # and that it is accessing the correct global state manager
    assert d1.chronicler is Channel.chronicler

    # make another
    d3 = Channel(name="test.channel", detail=3)
    # verify the name was recorder correctly
    assert d3.name == "test.channel"
    # that its detail is set to the default value
    assert d3.detail == 3
    # and that it is accessing the correct global state manager
    assert d3.chronicler is Channel.chronicler

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
