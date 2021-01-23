#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Exercise combining two constraints using the operator "|"
    """

    # get the package
    import pyre.constraints
    # build a constraint
    less = pyre.constraints.isLess(value=0)
    greater = pyre.constraints.isGreater(value=1)
    constraint = less | greater

    # exercise with good values
    constraint.validate(-2)
    constraint.validate(2)

    # a case that should fail
    stranger = .5
    try:
        constraint.validate(stranger)
    except constraint.ConstraintViolationError as error:
        assert error.constraint == constraint
        assert error.value == stranger

    # another one
    stranger = 0
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

    # and another
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
