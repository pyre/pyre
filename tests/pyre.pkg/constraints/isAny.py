#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Exercise "isAny"
    """

    # get the package
    import pyre.constraints
    # build a constraint
    less = pyre.constraints.isLess(value=0)
    greater = pyre.constraints.isGreater(value=1)
    constraint = pyre.constraints.isAny(less, greater)

    # exercise with good values
    constraint.validate(-2)
    constraint.validate(2)

    # a case that should fail
    stranger = .5
    # attempt to
    try:
        # validate it
        constraint.validate(stranger)
        # which should fail
        assert False, "unreachable"
    # catch the error
    except constraint.ConstraintViolationError as error:
        # and check the error conditions
        assert error.constraint == constraint
        assert error.value == stranger

    # another one
    stranger = 0
    # attempt to
    try:
        # validate it
        constraint.validate(stranger)
        # which should fail
        assert False, "unreachable"
    # catch the error
    except constraint.ConstraintViolationError as error:
        # and check the error conditions
        assert error.constraint == constraint
        assert error.value == stranger

    # another one
    stranger = 1
    # attempt to
    try:
        # validate it
        constraint.validate(stranger)
        # which should fail
        assert False, "unreachable"
    # catch the error
    except constraint.ConstraintViolationError as error:
        # and check the error conditions
        assert error.constraint == constraint
        assert error.value == stranger

    # all done
    return constraint


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
