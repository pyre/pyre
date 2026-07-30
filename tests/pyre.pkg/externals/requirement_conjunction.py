#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Comma separated version clauses form a conjunction
"""


def test():
    """
    Parse a version window and verify all clauses must hold together
    """
    # support
    import pyre.externals

    # parse a version window
    ranged = pyre.externals.requirement.parse("hdf5>=1.12,<2")
    # the clauses are recorded in order
    assert ranged.clauses == ((">=", "1.12"), ("<", "2"))
    # the lower boundary is inside the window
    assert ranged.accepts(version="1.12")
    # as is anything between the bounds
    assert ranged.accepts(version="1.14.6")
    # versions below the window fail the first clause
    assert not ranged.accepts(version="1.8.23")
    # versions above the window fail the second
    assert not ranged.accepts(version="2.1.0")

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
