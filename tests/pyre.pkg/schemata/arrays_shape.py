#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an array with a declared shape takes only values with those extents, where an extent of
None takes any length along its axis
"""


def test() -> None:
    """
    Convert values of various shapes
    """
    # the schemata
    import pyre.schemata

    # make a converter
    schema = pyre.schemata.array(shape=(2, 2))

    # a 2x2 matrix
    assert schema.coerce([[1, 2], [3, 4]]) == ((1.0, 2.0), (3.0, 4.0))

    # each of these
    for value in ([[1, 2, 3], [4, 5, 6]], [[1, 2]], [1, 2], ()):
        # attempt to
        try:
            # convert it
            schema.coerce(value)
            # which should be unreachable
            assert False, value
        # if it is refused, as expected
        except schema.CastingError:
            # all good
            pass

    # any number of points in three dimensions
    points = pyre.schemata.array(shape=(None, 3))
    # takes a few
    assert points.coerce([[1, 2, 3], [4, 5, 6]]) == ((1.0, 2.0, 3.0), (4.0, 5.0, 6.0))
    # and none at all
    assert points.coerce(()) == ()
    # but not points in two dimensions
    try:
        # convert them
        points.coerce([[1, 2]])
        # which should be unreachable
        assert False, "unreachable"
    # if they are refused, as expected
    except points.CastingError:
        # all good
        pass
    # an array that must be empty
    empty = pyre.schemata.array(shape=(0,))
    # takes an empty value
    assert empty.coerce("") == ()

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
