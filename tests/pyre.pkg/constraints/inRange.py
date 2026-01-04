#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise "inRange"
"""


def test():
    import pyre.constraints

    constraint = pyre.constraints.inRange(low=0, high=1)

    constraint.validate(0)
    constraint.validate(0.1)
    constraint.validate(0.1)
    constraint.validate(0.9)

    stranger = 1
    try:
        constraint.validate(stranger)
    except constraint.ConstraintViolationError as error:
        assert error.constraint == constraint
        assert error.value == stranger

    return constraint


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
