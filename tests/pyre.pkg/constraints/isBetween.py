#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Exercise "isBetween"
    """

    # get the package
    import pyre.constraints
    # build a constraint
    constraint = pyre.constraints.isBetween(low=0, high=1)

    # exercise with good values
    constraint.validate(.1)
    constraint.validate(.1)
    constraint.validate(.9)

    # a case that should fail
    stranger = 0
    # attempt to
    try:
        # validate it
        constraint.validate(stranger)
        # which should fail
        assert False, "unreachable"
    # catch it
    except constraint.ConstraintViolationError as error:
        # check the error conditions
        assert error.constraint == constraint
        assert error.value == stranger

    # and another one
    stranger = 1
    # attempt to
    try:
        # validate it
        constraint.validate(stranger)
        # which should fail
        assert False, "unreachable"
    # catch it
    except constraint.ConstraintViolationError as error:
        # check the error conditions
        assert error.constraint == constraint
        assert error.value == stranger

    # all done
    return constraint


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
