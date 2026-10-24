#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that declaring an array with a rank and a shape that make no sense fires a firewall, since the
mistake is in the code that declares it
"""


def test() -> None:
    """
    Declare arrays with bad ranks and shapes
    """
    # the journal
    import journal

    # and the schemata
    import pyre.schemata

    # the firewall fires on purpose here; keep its report out of the way
    journal.firewall("pyre.schemata").device = journal.trash()
    # each of these
    for kwds in (
        {"rank": 0},
        {"rank": -1},
        {"rank": 1.5},
        {"rank": True},
        {"shape": ()},
        {"shape": (-1,)},
        {"shape": ("a",)},
        {"shape": 3},
        {"rank": 2, "shape": (3,)},
    ):
        # attempt to
        try:
            # declare an array
            pyre.schemata.array(**kwds)
            # which should be unreachable
            assert False, kwds
        # if the firewall fires, as expected
        except journal.FirewallError:
            # all good
            pass
    # while a consistent declaration is fine
    assert pyre.schemata.array(rank=2, shape=(None, 3)).shape == (None, 3)

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
