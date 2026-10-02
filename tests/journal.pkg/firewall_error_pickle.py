#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    The exception raised by a fatal firewall survives a trip through pickle, so that processes
    can hand it to each other
    """
    # externals
    import pickle

    # get the exception
    from journal.exceptions import FirewallError

    # make one
    error = FirewallError(
        headline="tests.journal.firewall: FIREWALL BREACHED!",
        channel="tests.journal.firewall",
        page=["nasty bug:", "    hello world!"],
        notes={"severity": "firewall", "code": "7"},
    )
    # send it through pickle
    clone = pickle.loads(pickle.dumps(error))

    # verify it is the right kind
    assert type(clone) is FirewallError
    # with the same summary
    assert str(clone) == str(error)
    # the same channel name
    assert clone.channel == error.channel
    # the same page
    assert clone.page == error.page
    # and the same notes
    assert clone.notes == error.notes

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
