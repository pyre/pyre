#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# verify we can derive from {Channel} and create independent channel factories
def test():
    """
    Verify there is no cross talk among the indices of different channel severities
    """

    # get the package
    from journal.Channel import Channel

    # three channel subclasses
    class info(Channel, active=False):
        """
        info channel
        """

    class warning(Channel, active=True):
        """
        warning channel
        """

    class error(Channel, active=True, fatal=True):
        """
        error channel
        """


    # make a couple of info channels
    info_1 = info("info.channel_1")
    info_2 = info("info.channel_2")

    # make a couple of warning channels
    warning_1 = warning("warning.channel_1")
    warning_2 = warning("warning.channel_2")

    # make a couple of error channels
    error_1 = error("error.channel_1")
    error_2 = error("error.channel_2")

    # check the states
    assert info_1.active == False
    assert info_2.active == False
    assert warning_1.active == True
    assert warning_2.active == True
    assert error_1.active == True
    assert error_2.active == True

    # fatality
    assert info_1.fatal == False
    assert info_2.fatal == False
    assert warning_1.fatal == False
    assert warning_2.fatal == False
    assert error_1.fatal == True
    assert error_2.fatal == True

    # get the info index
    infos = info.index
    # verify it has exactly two registered names
    assert len(infos) == 2
    # that one of them is "info.channel_1"
    assert "info.channel_1" in infos
    # and the other is "info.channel_2"
    assert "info.channel_2" in infos

    # repeat with the warning index
    warnings = warning.index
    # verify it has exactly two registered names
    assert len(warnings) == 2
    # that one of them is "warning.channel_1"
    assert "warning.channel_1" in warnings
    # and the other is "warning.channel_2"
    assert "warning.channel_2" in warnings

    # repeat with the error index
    errors = error.index
    # verify it has exactly two registered names
    assert len(errors) == 2
    # that one of them is "error.channel_1"
    assert "error.channel_1" in errors
    # and the other is "error.channel_2"
    assert "error.channel_2" in errors

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
