#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Exercise "isNegative"
    """

    # get the package
    import pyre.constraints
    # build a constraint
    constraint = pyre.constraints.isNegative()

    # exercise with a good value
    constraint.validate(-0.9)

    # a case that should fail
    stranger = 0
    try:
        constraint.validate(stranger)
    except constraint.ConstraintViolationError as error:
        assert error.constraint == constraint
        assert error.value == stranger

    # and another one
    stranger = 1
    # try to
    try:
        # validate it
        constraint.validate(stranger)
        # which should fail
        assert False, "unreachable"
    # catch the error
    except constraint.ConstraintViolationError as error:
        # verify the error conditions
        assert error.constraint == constraint
        assert error.value == stranger


    # all done
    return constraint


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
