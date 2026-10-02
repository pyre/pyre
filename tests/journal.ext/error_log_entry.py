#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    The exception handed back by a non-fatal error channel carries the entry it recorded
    """
    # get the bindings
    from journal import libjournal

    # make a channel
    channel = libjournal.Error("tests.journal.error")
    # send the output to the trash
    channel.device = libjournal.Trash()
    # make it non-fatal
    channel.fatal = False

    # record an entry and get the exception
    error = channel.log("the input is unusable", code="3")
    # check the summary
    assert str(error) == "tests.journal.error: application error"
    # the channel name
    assert error.channel == "tests.journal.error"
    # the page
    assert error.page == ["the input is unusable"]
    # and the notes
    assert error.notes["severity"] == "error"
    assert error.notes["code"] == "3"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
