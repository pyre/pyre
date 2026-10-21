#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Subtracting quantities with incompatible units is reported as a subtraction
"""


def test() -> None:
    """
    Subtract a time from a length, and check the operation the error names
    """
    # support
    from pyre.units.SI import meter, second
    from pyre.units.exceptions import CompatibilityError

    # carefully
    try:
        # subtract a time from a length
        meter - second
    # it must be refused
    except CompatibilityError as error:
        # as a subtraction
        assert error.operation == "subtraction", error.operation
    # if it is not refused at all
    else:
        # say so
        assert False, "subtracted a time from a length"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
