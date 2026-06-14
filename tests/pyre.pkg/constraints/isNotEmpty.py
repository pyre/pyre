#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise "isNotEmpty"
"""


def test():
    import pyre.constraints

    constraint = pyre.constraints.isNotEmpty()

    # non-empty containers pass
    constraint.validate(["one"])
    constraint.validate(["one", "two"])
    constraint.validate({"a": 1})

    # an empty container is rejected
    stranger = []
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
