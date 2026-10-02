#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    The name of a channel cannot be changed
    """
    # get the channel
    from journal.Informational import Informational as info

    # make one
    channel = info(name="tests.journal.name")
    # verify its name
    assert channel.name == "tests.journal.name"
    # attempt to
    try:
        # rename it
        channel.name = "foo"
        # which should fail
        assert False, "unreachable"
    # if all goes well
    except AttributeError:
        # no problem
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
