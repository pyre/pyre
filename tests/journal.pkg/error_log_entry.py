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
    # get the trash can
    from journal.Trash import Trash as trash

    # and the channel
    from journal.Error import Error as error

    # make a channel
    channel = error(name="tests.journal.error")
    # send the output to the trash
    channel.device = trash()
    # make it non-fatal
    channel.fatal = False

    # record an entry and get the exception
    complaint = channel.log("the input is unusable", code="3")
    # check the summary
    assert str(complaint) == "tests.journal.error: application error"
    # the channel name
    assert complaint.channel == "tests.journal.error"
    # the page
    assert complaint.page == ["the input is unusable"]
    # and the notes
    assert complaint.notes["severity"] == "error"
    assert complaint.notes["code"] == "3"

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
