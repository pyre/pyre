#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that dimensional conversions work as expected
"""


def test():
    """
    Convert text into quantities, and refuse what is not one
    """
    # support
    import pyre.schemata
    from pyre.units.SI import m, kg, s

    # create a descriptor
    descriptor = pyre.schemata.dimensional()

    # a unit by its name
    assert m == descriptor.coerce("meter")
    # and an expression with units
    assert 9.81 * kg * m / s**2 == descriptor.coerce("9.81*kg*m/s**2")

    # attempt to
    try:
        # coerce something that is not a quantity
        descriptor.coerce([1])
        # which should be unreachable
        assert False
    # if it is refused, as expected
    except descriptor.CastingError as error:
        # with the generic complaint
        assert str(error) == "could not coerce [1] into a dimensional quantity"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
