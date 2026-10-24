#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a sequence renders as json with each entry rendered by its schema, so numbers stay
numbers
"""


def test() -> None:
    """
    Render lists and tuples of numbers as json
    """
    # the schemata
    import pyre.schemata

    # a list of integers
    assert pyre.schemata.list(schema=pyre.schemata.int()).json([1, 2]) == [1, 2]
    # a tuple of floats
    assert pyre.schemata.tuple(schema=pyre.schemata.float()).json((1.0, 2.5)) == (1.0, 2.5)

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
