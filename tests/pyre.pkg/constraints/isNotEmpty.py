#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise "isNotEmpty"
    """
    # access the constraints
    import pyre.constraints

    # make one
    constraint = pyre.constraints.isNotEmpty()

    # non-empty containers pass: a list with one item
    constraint.validate(["one"])
    # a list with more
    constraint.validate(["one", "two"])
    # and a map
    constraint.validate({"a": 1})

    # an empty container
    stranger = []
    # must be rejected
    try:
        # so validating it
        constraint.validate(stranger)
        # can't succeed
        assert False, "unreachable"
    # and when it fails
    except constraint.ConstraintViolationError as error:
        # the error names the constraint
        assert error.constraint == constraint
        # and the value it refused
        assert error.value == stranger

    # all done
    return constraint


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
