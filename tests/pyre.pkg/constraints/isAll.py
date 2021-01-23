#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Exercise "isAll"
    """

    # get the package
    import pyre.constraints
    # build a constraint
    less = pyre.constraints.isLess(value=1)
    greater = pyre.constraints.isGreater(value=0)
    constraint = pyre.constraints.isAll(less, greater)

    # exercise it with passing values
    constraint.validate(0.1)
    constraint.validate(0.5)
    constraint.validate(0.9)

    # a case that should fail
    stranger = 1
    # attempt to
    try:
        # give it a shot
        constraint.validate(stranger)
        # which should fail
        assert False, "unreachable"
    # catch it
    except constraint.ConstraintViolationError as error:
        # verify the error conditions
        assert error.constraint in [less, greater]
        assert error.value == stranger

    # and another one
    stranger = 0
    # attempt to
    try:
        # give it a shot
        constraint.validate(stranger)
    # catch it
    except constraint.ConstraintViolationError as error:
        # verify the error conditions
        assert error.constraint in [less, greater]
        assert error.value == stranger

    # all done
    return constraint


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
