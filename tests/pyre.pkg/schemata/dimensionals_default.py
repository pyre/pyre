#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a dimensional declared without a default has none, rather than a quantity of a
particular kind
"""


def test() -> None:
    """
    Declare dimensionals without defaults
    """
    # the schemata
    import pyre.schemata

    # a schema without a default
    assert pyre.schemata.dimensional().default is None
    # nor does declaring its units give it one
    assert pyre.schemata.dimensional(units=pyre.units.SI.meter).default is None

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
